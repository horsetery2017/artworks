const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),{spawn}=require('node:child_process');
const root=path.resolve(__dirname,'..'),qa=path.join(root,'qa'),profile=path.join(qa,'edge-profile');
const delay=ms=>new Promise(r=>setTimeout(r,ms));let browser,ws;const errors=[],checks=[];
const server=http.createServer((req,res)=>{const file=path.join(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\//,'')||'index.html');if(!fs.existsSync(file)||!fs.statSync(file).isFile())return res.writeHead(404).end();res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.svg':'image/svg+xml','.pdf':'application/pdf'})[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res)});
async function main(){
 await new Promise(r=>server.listen(0,'127.0.0.1',r));fs.mkdirSync(profile,{recursive:true});
 if(fs.existsSync(path.join(profile,'DevToolsActivePort')))fs.unlinkSync(path.join(profile,'DevToolsActivePort'));
 browser=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:'ignore'});
 const portFile=path.join(profile,'DevToolsActivePort');for(let i=0;i<100&&!fs.existsSync(portFile);i++)await delay(100);
 const port=fs.readFileSync(portFile,'utf8').split('\n')[0].trim(),tabs=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});let seq=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.responseReceived'&&m.params.response.status>=400)errors.push(m.params.response.url)};
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 const ev=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
 const assert=(condition,label)=>{if(!condition)throw Error(label);checks.push(label)};
 const shot=async name=>{const r=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(qa,name+'.png'),Buffer.from(r.data,'base64'))};
 await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
 for(const [name,width,height] of [['desktop',1440,1000],['mobile',393,852],['small-mobile',320,740]]){
  await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:name==='mobile'});
  await call('Page.navigate',{url:`http://127.0.0.1:${server.address().port}/`});await delay(500);
  await ev(`Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>{i.loading='eager';return i.decode()})).then(()=>document.fonts.ready).then(()=>true)`);
  assert(await ev('document.querySelectorAll(".work-card").length===8'),name+' eight artworks');
  assert(await ev('JSON.parse(document.querySelector("#work-data").textContent).every(w=>w.title_en&&w.category_en&&w.description_en&&w.images.every(i=>i.label_en))'),name+' bilingual artwork metadata');
  assert(await ev('[...document.querySelectorAll(".work-card")].every(c=>c.querySelector("h3 [lang=en]"))'),name+' bilingual artwork titles rendered');
  assert(await ev('document.querySelectorAll(".bio-zh p").length===3 && document.querySelectorAll(".bio-en p").length===3 && document.querySelector(".bio-en").textContent.includes("Joongbu University")'),name+' complete bilingual artist biography');
  assert(await ev('document.documentElement.scrollWidth<=innerWidth'),name+' no horizontal overflow');
  await shot(name);
  const metrics=await call('Page.getLayoutMetrics');const full=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width,height:Math.ceil(metrics.cssContentSize.height),scale:1}});fs.writeFileSync(path.join(qa,name+'-full.png'),Buffer.from(full.data,'base64'));
  await ev('document.querySelector("[data-open]").click()');assert(await ev('document.querySelector("dialog").open'),name+' dialog opens');assert(await ev('document.querySelector("#dialog-title [lang=en]").textContent==="Zero-Sum World" && !!document.querySelector("#dialog-description [lang=en]").textContent'),name+' bilingual dialog');await delay(200);await shot(name+'-dialog');
  await ev('document.querySelector("#next-work").click()');assert(await ev('document.querySelector("#dialog-counter").textContent.includes("03")'),name+' next artwork');
  await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});assert(await ev('!document.querySelector("dialog").open'),name+' escape closes');
  await ev('document.querySelectorAll("[data-variant]")[1].click();document.querySelectorAll("[data-variant]")[1].closest(".work-card").querySelector("[data-open]").click()');assert(await ev('document.querySelectorAll(".view-thumb")[1].getAttribute("aria-pressed")==="true"'),name+' second view retained');
  await ev('document.querySelector("dialog").close()');
 }
 await call('Page.navigate',{url:require('node:url').pathToFileURL(path.join(root,'index.html')).href});await delay(400);await ev('document.querySelector("[data-open]").click()');assert(await ev('document.querySelector("dialog").open'),'file URL opens without server');
 assert(errors.length===0,'no browser errors');await call('Browser.close');fs.writeFileSync(path.join(qa,'report.json'),JSON.stringify({checks,errors},null,2));console.log(JSON.stringify({checks,errors},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>{ws?.close();if(browser?.exitCode===null)browser.kill();server.close()});

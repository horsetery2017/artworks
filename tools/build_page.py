"""Build a portable, buildless GitHub Pages portfolio from source metadata."""
from pathlib import Path
import html
import json

ROOT=Path(__file__).resolve().parents[1]
works=json.loads((ROOT/'works.json').read_text(encoding='utf-8'))
manifest={x['slug']:x for x in json.loads((ROOT/'assets/image-manifest.json').read_text(encoding='utf-8'))}
esc=html.escape

def image(slug,alt,eager=False,css=''):
    entry=manifest[slug]['preview']
    return (f'<img src="{entry["path"]}" width="{entry["width"]}" height="{entry["height"]}" '
            f'alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" '
            f'decoding="async" {"fetchpriority=high" if eager else ""} {css}>')

cards=[]
index=[]
for i,w in enumerate(works):
    number=f'{i+1:02d}'
    subtitle=f'<span class="subtitle">（{esc(w["subtitle"])}）</span>' if w.get('subtitle') else ''
    variant=''
    if len(w['images'])>1:
        variant='<div class="variant-switch" aria-label="作品观看角度">'+''.join(
            f'<button type="button" data-variant="{j}" data-work="{w["id"]}" aria-pressed="{str(j==0).lower()}">{esc(im["label"])}</button>'
            for j,im in enumerate(w['images']))+'</div>'
    cards.append(f'''<article class="work-card" id="work-{w['id']}">
  <div class="work-visual">
    <button class="image-button" type="button" data-open="{w['id']}" aria-label="查看《{esc(w['title'])}》大图">
      {image(w['images'][0]['slug'], w['title']+' · '+w['images'][0]['label'])}
    </button>
    {variant}
  </div>
  <div class="work-heading"><span class="work-number">{number}</span><h3>{esc(w['title'])}{subtitle}</h3></div>
  <p class="work-category">{esc(w['category'])}</p>
  <p class="work-description">{esc(w['description'])}</p>
  <div class="work-foot"><button class="open-text" type="button" data-open="{w['id']}">查看作品 <span aria-hidden="true">↗</span></button><span class="work-view-count">{len(w['images']):02d} 幅图像</span></div>
</article>''')
    index.append(f'<li><a href="#work-{w["id"]}"><span class="index-no">{number}</span><span>{esc(w["title"])}</span><span aria-hidden="true">↗</span></a></li>')

page='''<!doctype html>
<html lang="zh-CN">
<head>
 <meta charset="utf-8">
 <meta name="viewport" content="width=device-width,initial-scale=1">
 <meta name="theme-color" content="#f6f4ee">
 <meta name="description" content="陈国军作品选集：飞翔矩阵、零和世界、游于艺之洛伦兹吸引子、王小波与陈清扬、以物形诗、向量空间与AI虫子。装置、互动与数字图像。">
 <meta property="og:title" content="陈国军 · 作品选集">
 <meta property="og:description" content="八件作品，九幅图像。装置、互动与数字图像的作品记录。">
 <meta property="og:type" content="website">
 <meta property="og:image" content="assets/images/zero-sum-preview.webp">
 <title>陈国军 · 作品选集 / CHEN GUOJUN</title>
 <link rel="icon" href="favicon.svg" type="image/svg+xml">
 <link rel="stylesheet" href="style.css">
 <script defer src="app.js"></script>
</head>
<body id="top">
<a class="skip-link" href="#works">跳到作品</a>
<div class="shell">
 <header class="site-header">
  <a class="brand" href="#top" aria-label="陈国军作品集首页"><span class="brand-zh">陈国军</span><span class="brand-en">CHEN<br>GUOJUN</span></a>
  <nav class="nav" aria-label="主导航"><a href="#works">作品</a><a href="#index">目录</a><a href="#colophon">图录</a><a class="pdf-link" href="assets/chen-guojun-selected-works.pdf" target="_blank" rel="noopener"><span class="pdf-word">原始 </span>PDF <span aria-hidden="true">↗</span></a></nav>
 </header>
 <main>
  <section class="hero" aria-labelledby="artist-name">
   <div class="hero-copy">
    <div class="eyebrow">SELECTED WORKS / 作品选集</div>
    <h1 id="artist-name">陈国军</h1>
    <p class="artist-roman">CHEN GUOJUN</p>
    <p class="hero-description">装置、互动与数字图像。<br>一份关于空间、界面与物的作品记录。</p>
    <div class="hero-bottom"><a class="browse-link" href="#works">浏览作品 <span aria-hidden="true">↓</span></a><div class="hero-count">08<span>件作品 / 09 幅图像</span></div></div>
   </div>
   <figure class="hero-art">
    <button class="image-button" type="button" data-open="zero-sum" aria-label="查看《零和世界》大图">__HERO__</button>
    <figcaption class="hero-caption"><strong>零和世界</strong><span>02 / 08 · 数字图像</span></figcaption>
   </figure>
  </section>
  <section class="catalogue" id="works" aria-labelledby="works-title">
   <div class="section-top"><div><span class="micro">A SELECTION / 01—08</span><h2 class="section-title" id="works-title">作品</h2></div><div class="section-aside">循图像，进入作品。<br>点击查看完整大图</div></div>
   <div class="work-grid">__CARDS__</div>
  </section>
  <section class="index-section" id="index" aria-labelledby="index-title">
   <div><span class="micro">WORK INDEX</span><h2 class="section-title" id="index-title">目录</h2></div>
   <ol class="index-list">__INDEX__</ol>
  </section>
  <section class="colophon" id="colophon" aria-labelledby="colophon-title">
   <div><span class="micro">COLOPHON</span><h2 id="colophon-title">关于这个选集</h2></div>
   <div class="colophon-content">
    <p>本页整理《陈国军部分作品》中的八件作品与九幅图像。《向量空间》保留两个观看视角；作品图像按原始比例呈现。</p>
    <p class="colophon-note">作品名称据原始图录。简短图像说明为网页整理文字。原资料未提供的创作年份、尺寸与艺术家履历，未在此页补写。</p>
    <a class="download" href="assets/chen-guojun-selected-works.pdf" download="陈国军部分作品.pdf">下载原始作品集 <span>PDF · 11.2 MB <span aria-hidden="true">↗</span></span></a>
   </div>
  </section>
 </main>
 <footer class="site-footer"><span>陈国军 / CHEN GUOJUN</span><span>SELECTED WORKS<br>作品图像与名称据原始图录整理</span></footer>
</div>
<dialog id="work-dialog" aria-labelledby="dialog-title">
 <div class="dialog-top"><span id="dialog-counter">作品</span><button class="close-dialog" type="button" aria-label="关闭大图">×</button></div>
 <div class="dialog-body">
  <div class="dialog-figure"><img id="dialog-image" alt=""></div>
  <div class="dialog-info"><h2 id="dialog-title"></h2><span class="dialog-category" id="dialog-category"></span><p class="dialog-description" id="dialog-description"></p><div class="dialog-views" id="dialog-views" aria-label="选择观看视角"></div><div class="dialog-source" id="dialog-source"></div><div class="dialog-links"><a id="original-image-link" target="_blank" rel="noopener">单独查看原图 ↗</a><a id="source-page-link" target="_blank" rel="noopener">图录对应页 ↗</a></div><div class="dialog-navigation"><button type="button" id="previous-work">← 上一件</button><button type="button" id="next-work">下一件 →</button></div></div>
 </div>
</dialog>
<noscript><div class="shell no-script">作品图像与名称可直接浏览；启用 JavaScript 后可点击放大。也可以<a href="assets/chen-guojun-selected-works.pdf">打开完整 PDF</a>。</div></noscript>
<script type="application/json" id="work-data">__DATA__</script>
</body>
</html>
'''
page=page.replace('__HERO__',image('zero-sum','零和世界 · 黑白球体构成的数字图像',True))
page=page.replace('__CARDS__','\n'.join(cards)).replace('__INDEX__','\n'.join(index))
page=page.replace('__DATA__',json.dumps(works,ensure_ascii=False).replace('</','<\\/'))
(ROOT/'index.html').write_text(page,encoding='utf-8')
(ROOT/'.nojekyll').touch()
print('Built index.html:',len(works),'work entries,',sum(len(w['images']) for w in works),'source images.')

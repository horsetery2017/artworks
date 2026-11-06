"""Build a portable, buildless GitHub Pages portfolio from source metadata."""
from pathlib import Path
import html
import json

ROOT=Path(__file__).resolve().parents[1]
works=json.loads((ROOT/'works.json').read_text(encoding='utf-8'))
artist=json.loads((ROOT/'artist.json').read_text(encoding='utf-8'))
manifest={x['slug']:x for x in json.loads((ROOT/'assets/image-manifest.json').read_text(encoding='utf-8'))}
esc=html.escape

def bi(zh,en):
    return f'{esc(zh)}<span class="en" lang="en">{esc(en)}</span>'

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
        variant='<div class="variant-switch" aria-label="作品观看角度 / Artwork viewpoints">'+''.join(
            f'<button type="button" data-variant="{j}" data-work="{w["id"]}" aria-pressed="{str(j==0).lower()}">{bi(im["label"],im["label_en"])}</button>'
            for j,im in enumerate(w['images']))+'</div>'
    cards.append(f'''<article class="work-card" id="work-{w['id']}">
  <div class="work-visual">
    <button class="image-button" type="button" data-open="{w['id']}" aria-label="查看《{esc(w['title'])}》大图 / View {esc(w['title_en'])}">
      {image(w['images'][0]['slug'], w['title']+' / '+w['title_en']+' · '+w['images'][0]['label']+' / '+w['images'][0]['label_en'])}
    </button>
    {variant}
  </div>
  <div class="work-heading"><span class="work-number">{number}</span><h3>{esc(w['title'])}{subtitle}<span class="en" lang="en">{esc(w['title_en'])}{' ('+esc(w['subtitle_en'])+')' if w.get('subtitle_en') else ''}</span></h3></div>
</article>''')
    index.append(f'<li><a href="#work-{w["id"]}"><span class="index-no">{number}</span><span>{bi(w["title"],w["title_en"])}</span><span aria-hidden="true">↗</span></a></li>')

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
  <nav class="nav" aria-label="主导航"><a href="#works">作品</a><a href="#about">关于</a><a class="pdf-link" href="assets/chen-guojun-selected-works.pdf" target="_blank" rel="noopener">PDF <span aria-hidden="true">↗</span></a></nav>
 </header>
 <main>
  <section class="hero" aria-labelledby="artist-name">
   <div class="hero-copy">
    <div class="eyebrow">SELECTED WORKS / 作品选集</div>
    <h1 id="artist-name">陈国军</h1>
    <p class="artist-roman">CHEN GUOJUN</p>
    <p class="hero-description">写诗也写代码。<br>将图视为符，也视符为图。</p>
    <div class="hero-bottom"><a class="browse-link" href="#works">浏览作品 <span aria-hidden="true">↓</span></a></div>
   </div>
   <figure class="hero-art">
    <button class="image-button" type="button" data-open="zero-sum" aria-label="查看《零和世界》大图">__HERO__</button>
    <figcaption class="hero-caption"><strong>零和世界</strong></figcaption>
   </figure>
  </section>
  <section class="artist-section" id="about" aria-labelledby="about-title">
   <h2 class="section-title" id="about-title">个人简介</h2>
   <div class="artist-biography">__BIOGRAPHY__</div>
  </section>
  <section class="catalogue" id="works" aria-labelledby="works-title">
   <div class="section-top"><h2 class="section-title" id="works-title">作品</h2></div>
   <div class="work-grid">__CARDS__</div>
  </section>
  <section class="colophon" id="colophon" aria-labelledby="colophon-title">
   <div><span class="micro">COLOPHON</span><h2 id="colophon-title">关于这个选集</h2></div>
   <div class="colophon-content">
    <p>本页整理《陈国军部分作品》中的八件作品与九幅图像。《向量空间》保留两个观看视角；作品图像按原始比例呈现。</p>
    <p class="colophon-note">作品名称据原始图录，英文名称为工作译名。作品说明为网页整理文字，个人简介由艺术家提供。</p>
    <a class="download" href="assets/chen-guojun-selected-works.pdf" download="陈国军部分作品.pdf">下载原始作品集 <span>PDF · 11.2 MB <span aria-hidden="true">↗</span></span></a>
   </div>
  </section>
 </main>
 <footer class="site-footer"><span>陈国军 / CHEN GUOJUN</span><a href="#top">回到顶部<span class="en" lang="en">Back to top ↑</span></a></footer>
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
copy={
 '跳到作品':'Skip to artworks', '作品':'Works', '目录':'Index', '图录':'Catalogue', '关于':'About',
 '个人简介':'Artist biography',
 '写诗也写代码。':'Poetry and code.',
 '将图视为符，也视符为图。':'Images as signs. Signs as images.',
 '作品名称据原始图录，英文名称为工作译名。作品说明为网页整理文字，个人简介由艺术家提供。':'Chinese artwork titles follow the source catalogue; English titles are working translations. Artwork descriptions were prepared for this website. The biography was provided by the artist.',
 '装置、互动与数字图像。':'Installations, interaction and digital imagery.',
 '一份关于空间、界面与物的作品记录。':'A record of works exploring space, interfaces and objects.',
 '浏览作品':'Browse works', '件作品 / 09 幅图像':'works / 09 images',
 '零和世界':'Zero-Sum World', '02 / 08 · 数字图像':'02 / 08 · Digital image',
 '循图像，进入作品。':'Enter the works through their images.', '点击查看完整大图':'Click to view full images',
 '关于这个选集':'About this selection',
 '本页整理《陈国军部分作品》中的八件作品与九幅图像。《向量空间》保留两个观看视角；作品图像按原始比例呈现。':'This page presents eight works and nine images from Selected Works by Chen Guojun. Vector Space includes two viewpoints; all artwork images retain their original proportions.',
 '作品名称据原始图录。简短图像说明为网页整理文字。原资料未提供的创作年份、尺寸与艺术家履历，未在此页补写。':'Chinese titles follow the source catalogue. English titles and brief image descriptions were prepared for this website. Dates, dimensions and an artist biography were not supplied and have not been added.',
 '下载原始作品集':'Download source catalogue', '作品图像与名称据原始图录整理':'Artwork images and titles compiled from the source catalogue',
 '单独查看原图 ↗':'Open full-size image ↗', '图录对应页 ↗':'Source catalogue page ↗',
 '← 上一件':'← Previous work', '下一件 →':'Next work →',
}
# Translate text nodes in the page template, before inserting bilingual artwork cards.
import re
page=re.sub(r'>([^<>]+)<',lambda m:'>'+bi(m[1],copy[m[1]])+'<' if m[1] in copy else m[0],page)
page=page.replace('浏览作品 <span',bi('浏览作品','Browse works')+' <span')
page=page.replace('下载原始作品集 <span',bi('下载原始作品集','Download source catalogue')+' <span')
page=page.replace('A SELECTION / 01—08','作品选集 / A SELECTION / 01—08')
page=page.replace('>WORK INDEX<','>作品目录 / WORK INDEX<').replace('>COLOPHON<','>图录说明 / COLOPHON<')
page=page.replace('>SELECTED WORKS<br>','>作品选集 / SELECTED WORKS<br>')
page=page.replace('<span class="pdf-word">原始 </span>PDF','<span class="pdf-word">原始 / Original </span>PDF')
page=page.replace('件作品 / 09 幅图像</span>','件作品 / 09 幅图像<span class="en" lang="en">works / 09 images</span></span>')
for zh,en in {'主导航':'Main navigation','陈国军作品集首页':'Chen Guojun portfolio home','查看《零和世界》大图':'View Zero-Sum World','关闭大图':'Close image viewer','选择观看视角':'Choose a viewpoint','作品观看角度':'Artwork viewpoints'}.items():
 page=page.replace(f'aria-label="{zh}"',f'aria-label="{zh} / {en}"')
page=page.replace('作品图像与名称可直接浏览；启用 JavaScript 后可点击放大。也可以',bi('作品图像与名称可直接浏览；启用 JavaScript 后可点击放大。','Artwork images and titles are available without JavaScript. Enable JavaScript to use the image viewer.'))
page=page.replace('打开完整 PDF',bi('打开完整 PDF','Open the complete PDF'))
page=page.replace('陈国军 · 作品选集 / CHEN GUOJUN','陈国军 · 作品选集 / CHEN GUOJUN · SELECTED WORKS')
page=page.replace('content="陈国军 · 作品选集"','content="陈国军 · 作品选集 / Chen Guojun · Selected Works"')
page=page.replace('装置、互动与数字图像。">','装置、互动与数字图像。 / Chen Guojun: selected installations, interactive works and digital imagery.">')
page=page.replace('八件作品，九幅图像。装置、互动与数字图像的作品记录。','八件作品，九幅图像。装置、互动与数字图像的作品记录。 / Eight works, nine images. Installations, interaction and digital imagery.')
page=page.replace('__HERO__',image('zero-sum','零和世界 / Zero-Sum World · 黑白球体构成的数字图像 / A digital image of black and white spheres',True))
page=page.replace('__CARDS__','\n'.join(cards)).replace('__INDEX__','\n'.join(index))
page=page.replace('__BIOGRAPHY__','<div class="bio-zh" lang="zh-CN">'+''.join(f'<p>{esc(p)}</p>' for p in artist['biography'])+'</div><div class="bio-en" lang="en">'+''.join(f'<p>{esc(p)}</p>' for p in artist['biography_en'])+'</div>')
page=page.replace('__DATA__',json.dumps(works,ensure_ascii=False).replace('</','<\\/'))
(ROOT/'index.html').write_text(page,encoding='utf-8')
(ROOT/'.nojekyll').touch()
print('Built index.html:',len(works),'work entries,',sum(len(w['images']) for w in works),'source images.')

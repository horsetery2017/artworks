"""Generate independent English and Chinese static pages for GitHub Pages."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
works = json.loads((ROOT / 'works.json').read_text(encoding='utf-8'))
artist = json.loads((ROOT / 'artist.json').read_text(encoding='utf-8'))
manifest = {item['slug']: item for item in json.loads((ROOT / 'assets/image-manifest.json').read_text(encoding='utf-8'))}
esc = html.escape


def build(language):
    english = language == 'en'
    lang = 'en' if english else 'zh-CN'
    filename = 'index.html' if english else 'zh.html'
    def text(zh, en):
        return en if english else zh
    def field(item, name):
        return item[name + '_en'] if english else item[name]
    def image(slug, alt, eager=False):
        item = manifest[slug]['preview']
        return (f'<img src="{item["path"]}" width="{item["width"]}" height="{item["height"]}" '
                f'alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" '
                f'{"fetchpriority=high" if eager else ""}>')

    cards = []
    for i, work in enumerate(works):
        title = field(work, 'title')
        subtitle = f'<span class="subtitle">{esc(field(work, "subtitle"))}</span>' if work.get('subtitle') else ''
        variants = ''
        if len(work['images']) > 1:
            buttons = ''.join(
                f'<button type="button" data-variant="{j}" data-work="{work["id"]}" aria-pressed="{str(j == 0).lower()}">{esc(field(im, "label"))}</button>'
                for j, im in enumerate(work['images']))
            variants = f'<div class="variant-switch" aria-label="{text("作品观看角度", "Artwork viewpoints")}">{buttons}</div>'
        label = text(f'查看《{title}》大图', f'View {title}')
        alt = title + ' · ' + field(work['images'][0], 'label')
        cards.append(f'''<article class="work-card" id="work-{work['id']}">
 <div class="work-visual"><button class="image-button" type="button" data-open="{work['id']}" aria-label="{esc(label)}">{image(work['images'][0]['slug'], alt)}</button>{variants}</div>
 <div class="work-heading"><span class="work-number">{i + 1:02d}</span><h3>{esc(title)}{subtitle}</h3></div>
</article>''')

    en_current = ' aria-current="page"' if english else ''
    zh_current = '' if english else ' aria-current="page"'
    language_switch = f'''<div class="language-switch" role="group" aria-label="{text('语言', 'Language')}"><a href="index.html" lang="en" hreflang="en"{en_current}>EN</a><span aria-hidden="true">/</span><a href="zh.html" lang="zh-CN" hreflang="zh-CN"{zh_current}>中文</a></div>'''
    name = field(artist, 'name')
    biography = ''.join(f'<p>{esc(p)}</p>' for p in field(artist, 'biography'))
    hero_title = field(works[1], 'title')
    hero_alt = text('零和世界 · 黑白球体构成的数字图像', 'Zero-Sum World · A digital image of black and white spheres')
    title = text('陈国军 · 作品选集', 'Chen Guojun · Selected Works')
    description = text('陈国军的作品与个人简介：数字媒体、互动装置与电子游戏。', 'Selected works and biography of Chen Guojun: digital media, interactive installations and video games.')
    note = text('作品名称据原始图录，英文名称为工作译名。作品说明为网页整理文字，个人简介由艺术家提供。', 'Chinese artwork titles follow the source catalogue; English titles are working translations. Artwork descriptions were prepared for this website. The biography was provided by the artist.')
    data = json.dumps(works, ensure_ascii=False).replace('</', '<\\/')
    page = f'''<!doctype html>
<html lang="{lang}">
<head>
 <meta charset="utf-8">
 <meta name="viewport" content="width=device-width,initial-scale=1">
 <meta name="theme-color" content="#faf9f6">
 <meta name="description" content="{esc(description)}">
 <meta property="og:title" content="{esc(title)}">
 <meta property="og:description" content="{esc(description)}">
 <meta property="og:type" content="website">
 <meta property="og:locale" content="{'en_US' if english else 'zh_CN'}">
 <meta property="og:image" content="assets/images/zero-sum-preview.webp">
 <title>{esc(title)}</title>
 <link rel="alternate" hreflang="en" href="index.html">
 <link rel="alternate" hreflang="zh-CN" href="zh.html">
 <link rel="alternate" hreflang="x-default" href="index.html">
 <link rel="icon" href="favicon.svg" type="image/svg+xml">
 <link rel="stylesheet" href="style.css">
 <script defer src="app.js"></script>
</head>
<body id="top">
<a class="skip-link" href="#works">{text('跳到作品', 'Skip to artworks')}</a>
<div class="shell">
 <header class="site-header">
  <a class="brand" href="{filename}" aria-label="{text('陈国军作品集首页', 'Chen Guojun portfolio home')}"><span class="brand-name">{esc(name)}</span></a>
  <div class="header-links"><nav class="nav" aria-label="{text('主导航', 'Main navigation')}"><a href="#works">{text('作品', 'Works')}</a><a href="#about">{text('关于', 'About')}</a><a href="assets/chen-guojun-selected-works.pdf" target="_blank" rel="noopener">PDF ↗</a></nav>{language_switch}</div>
 </header>
 <main>
  <section class="hero" aria-labelledby="artist-name">
   <div class="hero-copy">
    <div class="eyebrow">{text('作品选集', 'SELECTED WORKS')}</div>
    <h1 id="artist-name">{esc(name)}</h1>
    <p class="hero-description">{text('写诗也写代码。', 'Poetry and code.')}<br>{text('将图视为符，也视符为图。', 'Images as signs. Signs as images.')}</p>
    <div class="hero-bottom"><a class="browse-link" href="#works">{text('浏览作品', 'Browse works')} <span aria-hidden="true">↓</span></a></div>
   </div>
   <figure class="hero-art"><button class="image-button" type="button" data-open="zero-sum" aria-label="{esc(text('查看《零和世界》大图', 'View Zero-Sum World'))}">{image('zero-sum', hero_alt, True)}</button><figcaption class="hero-caption"><strong>{esc(hero_title)}</strong></figcaption></figure>
  </section>
  <section class="artist-section" id="about" aria-labelledby="about-title">
   <h2 class="section-title" id="about-title">{text('个人简介', 'About')}</h2>
   <div class="artist-biography">{biography}</div>
  </section>
  <section class="catalogue" id="works" aria-labelledby="works-title">
   <div class="section-top"><h2 class="section-title" id="works-title">{text('作品', 'Works')}</h2></div>
   <div class="work-grid">{''.join(cards)}</div>
  </section>
  <section class="colophon" aria-label="{text('图录说明', 'Catalogue notes')}"><div class="colophon-content"><p class="colophon-note">{esc(note)}</p><a class="download" href="assets/chen-guojun-selected-works.pdf" download="chen-guojun-selected-works.pdf">{text('下载原始作品集', 'Download source catalogue')} <span>PDF · 11.2 MB ↗</span></a></div></section>
 </main>
 <footer class="site-footer"><span>{esc(name)}</span><a href="#top">{text('回到顶部', 'Back to top')} ↑</a></footer>
</div>
<dialog id="work-dialog" aria-labelledby="dialog-title">
 <div class="dialog-top"><span id="dialog-counter">{text('作品', 'Work')}</span><button class="close-dialog" type="button" aria-label="{text('关闭大图', 'Close image viewer')}">×</button></div>
 <div class="dialog-body"><div class="dialog-figure"><img id="dialog-image" alt=""></div>
 <div class="dialog-info"><h2 id="dialog-title"></h2><span class="dialog-category" id="dialog-category"></span><p class="dialog-description" id="dialog-description"></p><div class="dialog-views" id="dialog-views" aria-label="{text('选择观看视角', 'Choose a viewpoint')}"></div><div class="dialog-source" id="dialog-source"></div><div class="dialog-links"><a id="original-image-link" target="_blank" rel="noopener">{text('单独查看大图', 'Open full-size image')} ↗</a><a id="source-page-link" target="_blank" rel="noopener">{text('图录对应页', 'Source catalogue page')} ↗</a></div><div class="dialog-navigation"><button type="button" id="previous-work">← {text('上一件', 'Previous work')}</button><button type="button" id="next-work">{text('下一件', 'Next work')} →</button></div></div></div>
</dialog>
<noscript><div class="shell no-script">{text('作品图像与名称可直接浏览；启用 JavaScript 后可点击放大。', 'Artwork images and titles are available without JavaScript. Enable JavaScript to use the image viewer.')} <a href="assets/chen-guojun-selected-works.pdf">{text('打开完整 PDF', 'Open the complete PDF')}</a></div></noscript>
<script type="application/json" id="work-data">{data}</script>
</body>
</html>
'''
    (ROOT / filename).write_text(page, encoding='utf-8')
    print(f'Built {filename}: {lang}, {len(works)} works')


for language in ('en', 'zh'):
    build(language)
(ROOT / '.nojekyll').touch()

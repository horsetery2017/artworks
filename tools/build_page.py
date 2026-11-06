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
        label = text(f'查看《{title}》大图', f'View {title}')
        images = ''.join(f'<figure><button class="image-button" type="button" data-open="{work["id"]}" data-view="{j}" aria-label="{esc(label+" · "+field(im,"label"))}">{image(im["slug"], title+" · "+field(im,"label"))}</button>'+ (f'<figcaption>{esc(field(im,"label"))}</figcaption>' if len(work['images'])>1 else '')+'</figure>' for j,im in enumerate(work['images']))
        cards.append(f'''<article class="work-card" id="work-{work['id']}">
 <div class="work-visual {'multiple-views' if len(work['images'])>1 else ''}">{images}</div>
 <div class="work-heading"><span class="work-number">{i + 1:02d}</span><h3>{esc(title)}{subtitle}</h3></div>
 <div class="work-details"><p class="work-year"><span>{text('年代', 'Year')}</span> <time>{esc(work['year'])}</time></p><div class="work-description">{''.join('<p>'+esc(paragraph)+'</p>' for paragraph in field(work, 'description').split(chr(10)))}</div></div>
</article>''')

    en_current = ' aria-current="page"' if english else ''
    zh_current = '' if english else ' aria-current="page"'
    language_switch = f'''<div class="language-switch" role="group" aria-label="{text('语言', 'Language')}"><a href="index.html" lang="en" hreflang="en"{en_current}>EN</a><span aria-hidden="true">/</span><a href="zh.html" lang="zh-CN" hreflang="zh-CN"{zh_current}>中文</a></div>'''
    name = field(artist, 'name')
    biography = ''.join(f'<p>{esc(p)}</p>' for p in field(artist, 'biography'))
    hero_alt = text('人物水墨绘画，背景有山水与弯月', 'An ink painting of a figure, with a landscape and crescent moon')
    title = text('陈国军 · 作品选集', 'Chen Guojun · Selected Works')
    description = text('陈国军的作品与个人简介：数字媒体、互动装置与电子游戏。', 'Selected works and biography of Chen Guojun: digital media, interactive installations and video games.')
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
 <link rel="stylesheet" href="style.css?v=portrait-70-20261106-4">
 <script defer src="app.js"></script>
</head>
<body id="top">
<a class="skip-link" href="#works">{text('跳到作品', 'Skip to artworks')}</a>
<div class="shell">
 <header class="site-header">
  <a class="brand" href="{filename}" aria-label="{text('陈国军作品集首页', 'Chen Guojun portfolio home')}"><span class="brand-name">{esc(name)}</span></a>
  <div class="header-links"><nav class="nav" aria-label="{text('主导航', 'Main navigation')}"><a href="#works">{text('作品', 'Works')}</a><a href="#about">{text('关于', 'About')}</a></nav>{language_switch}</div>
 </header>
 <main>
  <section class="hero" aria-labelledby="artist-name">
   <div class="hero-copy">
    <div class="eyebrow">{text('作品选集', 'SELECTED WORKS')}</div>
    <h1 id="artist-name">{esc(name)}</h1>
    <p class="hero-description">{text('写诗也写代码。', 'Poetry and code.')}<br>{text('将图视为符，也视符为图。', 'Images as signs. Signs as images.')}</p>
    <div class="hero-bottom"><a class="browse-link" href="#works">{text('浏览作品', 'Browse works')} <span aria-hidden="true">↓</span></a></div>
   </div>
   <figure class="hero-art hero-portrait"><img src="assets/images/works.jpg" width="1231" height="1114" alt="{esc(hero_alt)}" loading="eager" decoding="async" fetchpriority="high"></figure>
  </section>
  <section class="artist-section" id="about" aria-labelledby="about-title">
   <h2 class="section-title" id="about-title">{text('个人简介', 'About')}</h2>
   <div class="artist-biography">{biography}</div>
  </section>
  <section class="catalogue" id="works" aria-labelledby="works-title">
   <div class="section-top"><h2 class="section-title" id="works-title">{text('作品', 'Works')}</h2></div>
   <div class="work-grid">{''.join(cards)}</div>
  </section>
 </main>
 <footer class="site-footer"><span>{esc(name)}</span><a href="#top">{text('回到顶部', 'Back to top')} ↑</a></footer>
</div>
<dialog id="work-dialog" aria-labelledby="dialog-title">
 <div class="dialog-top"><span id="dialog-counter">{text('作品', 'Work')}</span><button class="close-dialog" type="button" aria-label="{text('关闭大图', 'Close image viewer')}">×</button></div>
 <div class="dialog-body"><div class="dialog-figure"><img id="dialog-image" alt=""></div>
 <div class="dialog-info"><h2 id="dialog-title"></h2><span class="dialog-category" id="dialog-category"></span><p class="dialog-year" id="dialog-year"></p><p class="dialog-description" id="dialog-description"></p><div class="dialog-views" id="dialog-views" aria-label="{text('选择观看视角', 'Choose a viewpoint')}"></div><div class="dialog-links"><a id="original-image-link" target="_blank" rel="noopener">{text('单独查看大图', 'Open full-size image')} ↗</a></div><div class="dialog-navigation"><button type="button" id="previous-work">← {text('上一件', 'Previous work')}</button><button type="button" id="next-work">{text('下一件', 'Next work')} →</button></div></div></div>
</dialog>
<noscript><div class="shell no-script">{text('作品图像与名称可直接浏览；启用 JavaScript 后可点击放大。', 'Artwork images and titles are available without JavaScript. Enable JavaScript to use the image viewer.')}</div></noscript>
<script type="application/json" id="work-data">{data}</script>
</body>
</html>
'''
    (ROOT / filename).write_text(page, encoding='utf-8')
    print(f'Built {filename}: {lang}, {len(works)} works')


for language in ('en', 'zh'):
    build(language)
(ROOT / '.nojekyll').touch()

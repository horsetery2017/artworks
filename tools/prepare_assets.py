"""Extract supplied PDF images without redrawing or retouching the artworks."""
from pathlib import Path
from io import BytesIO
import json
import shutil
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = next(p for p in ROOT.parent.glob('*.pdf') if p.name.startswith('\u9648\u56fd\u519b'))
doc = pymupdf.open(SOURCE)
mapping = [
    ('flight-matrix', 2, 21), ('zero-sum', 3, 24),
    ('wang-and-chen', 3, 25), ('lorenz', 4, 28),
    ('formal-machine', 5, 31), ('buffer-zone', 6, 34),
    ('vector-view-1', 7, 37), ('vector-view-2', 8, 40),
    ('ai-insect', 9, 43),
]
manifest = []
for slug, page, xref in mapping:
    source = doc.extract_image(xref)
    image = Image.open(BytesIO(source['image'])).convert('RGB')
    info = next(i for i in doc[page-1].get_image_info(xrefs=True) if i['xref'] == xref)
    a, b, c, d, *_ = info['transform']
    # Match the PDF's placed orientation, not the embedded JPEG orientation.
    if abs(a) < 0.001 and b > 0 and c < 0:
        image = image.transpose(Image.Transpose.ROTATE_270)
    entry = {'slug': slug, 'page': page, 'xref': xref, 'source_size': image.size}
    for suffix, limit, quality in [('preview', 1400, 88), ('full', 3000, 94)]:
        result = image.copy()
        result.thumbnail((limit, limit), Image.Resampling.LANCZOS)
        dest = ROOT / 'assets' / 'images' / f'{slug}-{suffix}.webp'
        result.save(dest, 'WEBP', quality=quality, method=6)
        entry[suffix] = {'path': str(dest.relative_to(ROOT)).replace('\\', '/'),
                         'width': result.width, 'height': result.height,
                         'bytes': dest.stat().st_size}
    manifest.append(entry)
shutil.copy2(SOURCE, ROOT / 'assets' / 'chen-guojun-selected-works.pdf')
(ROOT / 'assets' / 'image-manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Extracted {len(manifest)} images; preserved all PDF image orientations.')

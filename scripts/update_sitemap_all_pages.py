from pathlib import Path
from html import escape
import re
root=Path('/home/ubuntu/anioracle')
files=sorted(p.name for p in root.glob('*.html') if p.name not in {'404.html'})
old=(root/'sitemap.xml').read_text(encoding='utf-8')
urls=[]
for name in files:
    loc='https://anioracle.online/' if name=='index.html' else f'https://anioracle.online/{name}'
    urls.append(f'  <url><loc>{escape(loc)}</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>{"1.0" if name=="index.html" else "0.7"}</priority></url>')
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(urls)+'\n</urlset>\n'
(root/'sitemap.xml').write_text(xml,encoding='utf-8')
print(f'indexed {len(files)} public HTML pages')

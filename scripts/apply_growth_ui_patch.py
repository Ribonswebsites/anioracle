from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
text = index.read_text()

css_anchor = '''.sec-title { font-size: clamp(2.2rem, 8.5vw, 3.8rem); font-weight: 900; line-height: .95; letter-spacing: -.035em; text-align: center; margin-bottom: 12px; }'''
css_add = '''
/* Lightweight motion layer: no library, no extra requests, reduced-motion safe. */
.sec-title, .hero-title {
  background: linear-gradient(110deg, var(--snow) 20%, var(--pu3) 45%, var(--pk2) 60%, var(--snow) 80%);
  background-size: 240% auto;
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  animation: ao-text-shimmer 9s linear infinite;
}
.ao-marquee-viewport { overflow-x: auto; scrollbar-width: none; }
.ao-marquee-viewport::-webkit-scrollbar { display: none; }
.ao-marquee-track { display: inline-flex; width: max-content; animation: ao-marquee-right 42s linear infinite; will-change: transform; }
.ao-marquee-viewport:hover .ao-marquee-track, .ao-marquee-viewport:focus-within .ao-marquee-track { animation-play-state: paused; }
@keyframes ao-text-shimmer { to { background-position: -240% center; } }
@keyframes ao-marquee-right { from { transform: translateX(-50%); } to { transform: translateX(0); } }
@media (prefers-reduced-motion: reduce) { .sec-title, .hero-title, .ao-marquee-track { animation: none !important; } }
'''
if 'ao-text-shimmer' not in text:
    if css_anchor not in text:
        raise SystemExit('CSS anchor not found')
    text = text.replace(css_anchor, css_anchor + css_add, 1)

# Remove footer entry points only; retain legal source pages in the repository.
text = re.sub(r'\s*<a href="(?:\./)?(?:terms|privacy|disclaimer|contact)\.html"[^>]*>.*?</a>', '', text, flags=re.S)

start = text.find('function renderCharList(elId, items, rankColor) {')
end = text.find('\nasync function loadMostPopular()', start)
if start == -1 or end == -1:
    raise SystemExit('renderCharList bounds not found')
fn = text[start:end]
if 'ao-marquee-track' not in fn:
    fn = fn.replace(
        "  el.innerHTML = `<div style=\"display:flex;gap:10px;overflow-x:auto;padding:0 16px 16px;scrollbar-width:none;-ms-overflow-style:none\">` +\n    items.slice(0, 20).map((c, i) => {",
        "  const cards = items.slice(0, 20).map((c, i) => {",
        1,
    )
    fn = fn.replace(
        "    }).join('') + `</div>`;\n}",
        "    }).join('');\n  el.innerHTML = `<div class=\"ao-marquee-viewport\" tabindex=\"0\" aria-label=\"Scrolling anime character rankings\"><div class=\"ao-marquee-track\" style=\"gap:10px;padding:0 16px 16px\">${cards}${cards}</div></div>`;\n}",
        1,
    )
    if 'ao-marquee-track' not in fn:
        raise SystemExit('renderCharList replacement failed')
    text = text[:start] + fn + text[end:]

index.write_text(text)

(root / 'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://anioracle.online/</loc><lastmod>2026-09-09</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
  <url><loc>https://anioracle.online/wiki.html</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://anioracle.online/fights-updated.html</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://anioracle.online/most-beautiful-v2-2.html</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://anioracle.online/most-popular-v3-3.html</loc><lastmod>2026-09-09</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://anioracle.online/most-hated-final.html</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>
  <url><loc>https://anioracle.online/wallpaper.html</loc><lastmod>2026-09-09</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>
</urlset>
''')
print('Applied footer cleanup, marquee motion, text shimmer, and expanded sitemap')

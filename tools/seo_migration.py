from pathlib import Path
from datetime import date
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
CONTENT_PAGES = [
    'index.html',
    'anime-character-database.html',
    'anime-power-levels.html',
    'strongest-anime-characters.html',
    'anime-vs-battles.html',
    'one-piece-oda-sbs-facts.html',
    'anime-character-heights.html',
    'anime-bounty-rankings.html',
    'anime-fashion-week.html',
    'anime-games.html',
    'wallpaper.html',
    'wiki.html',
    'fights-updated.html',
    'most-popular-v3-3.html',
    'most-hated-final.html',
    'most-beautiful-v2-2.html',
]

# Keep the homepage's site-name preference concise and consistent with its visible brand.
index = ROOT / 'index.html'
text = index.read_text(encoding='utf-8')
text = text.replace('<link rel="alternate" hreflang="x-default" href="https://anioracle.online/">', '<link rel="alternate" hreflang="x-default" href="https://anioracle.online/">\n<link rel="sitemap" type="application/xml" href="/sitemap.xml">')
text = text.replace('<meta name="author" content="AniOracle">', '<meta name="author" content="AniOracle">\n<meta name="application-name" content="AniOracle">')
# Remove the empty JSON-LD block that cannot help Google understand the page.
text = text.replace('<script type="application/ld+json">\n</script>\n', '')
# Replace the homepage list with real, crawlable editorial destinations rather than ten identical homepage URLs.
pattern = re.compile(r'<script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"ItemList".*?</script>', re.S)
content_items = [
    ('Anime Character Database', 'anime-character-database.html', 'Anime character profiles, aliases, abilities, heights, birthdays and series references.'),
    ('Anime Power Levels', 'anime-power-levels.html', 'Anime power levels, tiers, feats and character scaling references.'),
    ('Strongest Anime Characters', 'strongest-anime-characters.html', 'AniOracle editorial ranking of the strongest anime characters.'),
    ('Anime VS Battles', 'anime-vs-battles.html', 'Anime matchup analysis, feats, win conditions and battle breakdowns.'),
    ('One Piece Oda SBS Facts', 'one-piece-oda-sbs-facts.html', 'Author-confirmed One Piece SBS facts and character references.'),
    ('Anime Character Heights', 'anime-character-heights.html', 'Anime height references and comparison charts.'),
    ('Anime Bounty Rankings', 'anime-bounty-rankings.html', 'One Piece bounty references and rankings.'),
    ('Anime Games', 'anime-games.html', 'Anime game ratings for PC, console, mobile and upcoming releases.'),
    ('Anime Fashion Week', 'anime-fashion-week.html', 'Anime character outfit ratings and fashion analysis.'),
    ('Free Anime Wallpapers', 'wallpaper.html', 'Anime wallpapers for phone and desktop.'),
]
item_schema = {
    '@context': 'https://schema.org', '@type': 'ItemList',
    'name': 'Explore the AniOracle anime universe',
    'description': 'Crawlable AniOracle guides for anime characters, power levels, battles, facts, rankings, games and wallpapers.',
    'url': 'https://anioracle.online/',
    'numberOfItems': len(content_items),
    'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': name, 'url': f'https://anioracle.online/{url}', 'description': desc}
        for i, (name, url, desc) in enumerate(content_items, 1)
    ]
}
new_block = '<script type="application/ld+json">\n' + json.dumps(item_schema, ensure_ascii=False, separators=(',', ':')) + '\n</script>'
text = pattern.sub(new_block, text, count=1)
index.write_text(text, encoding='utf-8')

for filename in CONTENT_PAGES[1:]:
    path = ROOT / filename
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8')
    title_match = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    if not (title_match and desc_match and canonical_match):
        continue
    title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
    desc = re.sub(r'\s+', ' ', desc_match.group(1)).strip()
    canonical = canonical_match.group(1)
    additions = [
        f'<meta name="author" content="AniOracle">',
        f'<meta property="og:site_name" content="AniOracle">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        '<meta property="og:image" content="https://anioracle.online/anioracle-logo-1-1.png">',
        '<meta property="og:image:alt" content="AniOracle anime database and rankings">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        '<meta name="twitter:image" content="https://anioracle.online/anioracle-logo-1-1.png">',
        '<link rel="sitemap" type="application/xml" href="/sitemap.xml">',
    ]
    existing = html.lower()
    additions = [line for line in additions if line.lower() not in existing]
    webpage = {
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': title, 'description': desc, 'isPartOf': {'@id': 'https://anioracle.online/#website'}, 'inLanguage': 'en-US'},
            {'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'AniOracle', 'item': 'https://anioracle.online/'},
                {'@type': 'ListItem', 'position': 2, 'name': title.replace(' — AniOracle', '').replace(' | AniOracle', ''), 'item': canonical}
            ]}
        ]
    }
    additions.append('<script type="application/ld+json">' + json.dumps(webpage, ensure_ascii=False, separators=(',', ':')) + '</script>')
    html = html.replace('</head>', '\n' + '\n'.join(additions) + '\n</head>', 1)
    path.write_text(html, encoding='utf-8')

# Add a minimal WebPage node and sitemap link to the homepage if absent.
text = index.read_text(encoding='utf-8')
if '<link rel="sitemap" type="application/xml" href="/sitemap.xml">' not in text:
    text = text.replace('</head>', '<link rel="sitemap" type="application/xml" href="/sitemap.xml">\n</head>', 1)
index.write_text(text, encoding='utf-8')

urls = [f'https://anioracle.online/{filename}' if filename != 'index.html' else 'https://anioracle.online/' for filename in CONTENT_PAGES]
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url in urls:
    xml.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>')
xml.append('</urlset>')
(ROOT / 'sitemap.xml').write_text('\n'.join(xml) + '\n', encoding='utf-8')
(ROOT / 'robots.txt').write_text('# AniOracle robots.txt\nUser-agent: *\nAllow: /\nDisallow: /cdn-cgi/\n\nSitemap: https://anioracle.online/sitemap.xml\n', encoding='utf-8')

manifest = ROOT / 'manifest.json'
if manifest.exists():
    m = json.loads(manifest.read_text(encoding='utf-8'))
    m['description'] = 'AniOracle is a free anime database for character profiles, power levels, VS battles, rankings, facts, wallpapers and AI anime chat.'
    manifest.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(f'Updated AniOracle homepage signals, added structured data and social metadata to {len(CONTENT_PAGES)-1} editorial pages, and generated a {len(urls)}-URL sitemap plus robots.txt.')

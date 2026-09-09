from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'

text = INDEX.read_text(encoding='utf-8')

# Replace the broken/white splash treatment with a true full-bleed image background.
text = text.replace('''  object-fit: contain;\n  background: #ffffff;\n}\n.splash-poster {\n  position: absolute; inset: 0; z-index: 0;\n  width: 100%; height: 100%;\n  object-fit: contain;\n  background: #fff;\n  animation: splash-poster-in 1.2s var(--ease-out-expo) both;\n}''', '''  object-fit: cover;\n  background: #000007;\n}\n.splash-poster {\n  position: absolute; inset: 0; z-index: 0;\n  width: 100%; height: 100%;\n  object-fit: cover;\n  object-position: center center;\n  background: #000007;\n  animation: splash-poster-in 1.2s var(--ease-out-expo) both;\n}''')
text = text.replace('''#splash {\n  position: fixed; inset: 0; z-index: 9999;\n  background: #ffffff;''', '''#splash {\n  position: fixed; inset: 0; z-index: 9999;\n  background: #000007;''')
# Remove the malformed orphaned keyframe close left by the previous patch.
text = text.replace('''}\n  to { opacity: 0; transform: scale(1.05); }\n}\n.splash-petals''', '''}\n.splash-petals''')
# Ensure supplied artwork is the only visible splash layer.
marker = '''.splash-petals { position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 3; }'''
insert = '''/* The supplied splash artwork is the complete intro canvas. Keep branding overlays out of it. */\n#splash > .splash-ribons, #splash > div:last-child { display: none !important; }\n'''
if insert not in text:
    text = text.replace(marker, insert + marker)

# Add robust, scroll-aware motion and horizontal loop styles once.
motion_css = '''\n/* Scroll-aware motion system: every section enters from the left, then gently wiggles. */\n.ao-scroll-reveal {\n  opacity: 0;\n  transform: translate3d(-72px, 0, 0);\n  will-change: transform, opacity;\n}\n.ao-scroll-reveal.ao-visible {\n  opacity: 1;\n  transform: translate3d(0, 0, 0);\n  transition: opacity .72s var(--ease-out-expo), transform .72s var(--ease-out-expo);\n  animation: ao-heading-wiggle 4.8s ease-in-out 1s infinite alternate;\n}\n@keyframes ao-heading-wiggle {\n  0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); }\n  35% { transform: translate3d(7px, -2px, 0) rotate(.35deg); }\n  70% { transform: translate3d(-5px, 1px, 0) rotate(-.25deg); }\n}\n.ao-loop-strip {\n  scroll-behavior: auto !important;\n  overscroll-behavior-inline: contain;\n}\n.ao-loop-strip.ao-looping {\n  mask-image: linear-gradient(90deg, transparent 0, #000 3%, #000 97%, transparent 100%);\n}\n.ao-loop-strip.ao-loop-paused { animation-play-state: paused; }\n@media (prefers-reduced-motion: reduce) {\n  .ao-scroll-reveal, .ao-scroll-reveal.ao-visible { opacity: 1; transform: none; animation: none !important; transition: none !important; }\n}\n'''
if '/* Scroll-aware motion system:' not in text:
    text = text.replace('</style>', motion_css + '</style>', 1)

# Improve primary metadata and remove unsupported aggregate-rating claims.
text = text.replace('AniOracle — Anime Characters, Power Levels, VS Battles &amp; AI Chat | Free Forever', 'AniOracle | Free Anime Database, Character Power Levels, VS Battles &amp; AI Chat')
text = text.replace('AniOracle: the #1 free anime database.', 'AniOracle is a free anime database.')
text = text.replace('The #1 free anime database.', 'A free anime database.')
text = re.sub(r'\s*"aggregateRating":\{"@type":"AggregateRating","ratingValue":"4\.9","reviewCount":"2847","bestRating":"5","worstRating":"1"\},', '', text)

# Add a visible, crawlable topic hub before the footer.
seo_hub = '''\n<!-- ═══ SEO DISCOVERY HUB ═══ -->\n<section class="ao-seo-hub ao-scroll-reveal" aria-labelledby="anime-search-hub-title">\n  <div class="eyebrow-wrap"><div class="eyebrow-line"></div><div class="eyebrow"><span class="eyebrow-dot"></span>Free Anime Search Hub</div><div class="eyebrow-line r"></div></div>\n  <h2 id="anime-search-hub-title" class="sec-title"><span class="st-plain">Search Anime</span><span class="st-grad">Facts &amp; Power</span><span class="st-stroke">FREE FOREVER</span></h2>\n  <p class="sec-desc">Find free anime character profiles, power levels, rankings, battles, wiki facts, birthdays, heights, bounties, and author-confirmed One Piece SBS answers in one place.</p>\n  <div class="ao-seo-grid">\n    <a href="./wiki.html" class="ao-seo-card"><strong>Anime Character Database</strong><span>Character powers, abilities, anime appearances, birthdays, heights, and quick facts.</span></a>\n    <a href="./most-popular-v3-3.html" class="ao-seo-card"><strong>Strongest Anime Characters</strong><span>Compare the strongest characters from One Piece, Naruto, Dragon Ball, Bleach, and more.</span></a>\n    <a href="./fights-updated.html" class="ao-seo-card"><strong>Free Anime VS Battles</strong><span>Explore anime matchups, power scaling, feats, win conditions, and battle breakdowns.</span></a>\n    <a href="./wiki.html#oda-sbs" class="ao-seo-card"><strong>One Piece Oda SBS Facts</strong><span>Browse author Q&amp;A topics including character details, heights, birthdays, bounties, and bust-size reveals.</span></a>\n    <a href="./most-beautiful-v2-2.html" class="ao-seo-card"><strong>Most Beautiful Anime Characters</strong><span>Fan rankings and visual profiles across popular anime universes.</span></a>\n    <a href="./wallpaper.html" class="ao-seo-card"><strong>Free Anime Wallpapers</strong><span>Browse anime artwork and wallpapers for your phone and desktop.</span></a>\n  </div>\n  <div class="ao-search-questions" aria-label="Popular anime searches">\n    <span>oracle anime</span><span>anime character database</span><span>anime power levels</span><span>strongest anime characters</span><span>One Piece bust size revealed by Oda</span><span>free anime wiki</span><span>anime height chart</span><span>anime bounty rankings</span>\n  </div>\n</section>\n<style>\n.ao-seo-hub{padding:54px 16px 42px;background:linear-gradient(180deg,var(--bg),var(--bg2));text-align:center}\n.ao-seo-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;max-width:760px;margin:24px auto 18px;text-align:left}\n.ao-seo-card{display:flex;flex-direction:column;gap:7px;padding:15px;border:1px solid rgba(139,92,246,.22);border-radius:16px;background:rgba(139,92,246,.06);transition:transform .2s,border-color .2s,background .2s}\n.ao-seo-card:hover,.ao-seo-card:focus-visible{transform:translateY(-3px);border-color:rgba(236,72,153,.6);background:rgba(139,92,246,.12);outline:none}\n.ao-seo-card strong{font-size:.72rem;color:var(--snow);line-height:1.35}\n.ao-seo-card span{font-size:.58rem;color:var(--snow3);line-height:1.55}\n.ao-search-questions{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;max-width:760px;margin:0 auto;color:var(--snow4);font-size:.52rem}\n.ao-search-questions span{padding:5px 8px;border:1px solid var(--line);border-radius:99px}\n@media(max-width:480px){.ao-seo-grid{grid-template-columns:1fr}.ao-seo-hub{padding-left:14px;padding-right:14px}}\n</style>\n'''
anchor = '<!-- ═══ RIBONS FOOTER ═══ -->'
if 'id="anime-search-hub-title"' not in text:
    text = text.replace(anchor, seo_hub + '\n' + anchor, 1)

# Add the scroll/motion controller before the existing nav function.
controller = r'''\n/* ══ SCROLL MOTION + RIGHTWARD STRIP LOOP ══ */\n(function initAniOracleMotion(){\n  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n  var loopStates = new WeakMap();\n  function registerReveal(root){\n    if (!root) return;\n    var targets = root.querySelectorAll('.sec-title, .eyebrow-wrap, .sec-desc, .ao-seo-hub, .ao-seo-card, .hero-title, .hero-content, [data-motion]');\n    targets.forEach(function(el){ el.classList.add('ao-scroll-reveal'); });\n    if (reduce) { targets.forEach(function(el){ el.classList.add('ao-visible'); }); return; }\n    var io = new IntersectionObserver(function(entries){\n      entries.forEach(function(entry){\n        entry.target.classList.toggle('ao-visible', entry.isIntersecting);\n      });\n    }, {root: root, threshold: .12, rootMargin: '0px 0px -8% 0px'});\n    targets.forEach(function(el){ io.observe(el); });\n  }\n  function registerStrips(root){\n    if (!root || reduce) return;\n    root.querySelectorAll('[style*="overflow-x:auto"], [style*="overflow-x: auto"], .ao-loop-strip').forEach(function(strip){\n      if (loopStates.has(strip)) return;\n      strip.classList.add('ao-loop-strip');\n      var state = {paused:false, last:performance.now(), manualUntil:0};\n      loopStates.set(strip,state);\n      ['mouseenter','focusin','touchstart','pointerdown'].forEach(function(evt){ strip.addEventListener(evt,function(){ state.paused=true; state.manualUntil=performance.now()+1400; }); });\n      ['mouseleave','focusout','touchend','pointerup'].forEach(function(evt){ strip.addEventListener(evt,function(){ state.paused=false; state.manualUntil=performance.now()+900; }); });\n      strip.addEventListener('scroll',function(){ state.manualUntil=performance.now()+1200; },{passive:true});\n      strip.classList.add('ao-looping');\n      (function tick(now){\n        var dt=Math.min(34,now-state.last); state.last=now;\n        if (!state.paused && now>state.manualUntil && strip.scrollWidth>strip.clientWidth+8) {\n          strip.scrollLeft += dt*0.028;\n          if (strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 2) strip.scrollLeft=0;\n        }\n        requestAnimationFrame(tick);\n      })(performance.now());\n    });\n  }\n  function scan(){\n    document.querySelectorAll('.pg').forEach(function(pg){ registerReveal(pg); registerStrips(pg); });\n  }\n  window.addEventListener('DOMContentLoaded', function(){ scan(); setTimeout(scan,1200); setTimeout(scan,6500); });\n  window.setInterval(scan, 2500);\n})();\n'''
if 'SCROLL MOTION + RIGHTWARD STRIP LOOP' not in text:
    text = text.replace('/* ══════════════════════════════════\n   NAV\n══════════════════════════════════ */', controller + '\n/* ══════════════════════════════════\n   NAV\n══════════════════════════════════ */', 1)

INDEX.write_text(text, encoding='utf-8')

# Add canonical/description/robots metadata to every public HTML page missing it.
desc = {
    'wiki.html': 'Free anime wiki with character profiles, powers, abilities, birthdays, heights, and searchable anime facts from AniOracle.',
    'fights-updated.html': 'Explore free anime VS battles, matchup analysis, power scaling, feats, and win conditions across major anime series.',
    'most-beautiful-v2-2.html': 'Browse AniOracle fan rankings of the most beautiful anime characters from popular anime universes.',
    'most-popular-v3-3.html': 'Browse the most popular anime characters and fan-favorite rankings across One Piece, Naruto, Dragon Ball, Bleach, and more.',
    'most-hated-final.html': 'Explore the most hated anime characters and the story reasons fans rank them among anime villains and antagonists.',
    'wallpaper.html': 'Find free anime wallpapers and artwork for mobile and desktop from the AniOracle anime universe.',
    'contact.html': 'Contact AniOracle about the free anime database, character data, anime facts, and website feedback.',
    'privacy.html': 'Read the AniOracle privacy policy for this free fan-made anime website.',
    'terms.html': 'Read the AniOracle terms of use for this free fan-made anime website.',
    'disclaimer.html': 'Read the AniOracle fan-made anime content and rights disclaimer.'
}
for page, description in desc.items():
    path = ROOT / page
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8')
    canonical = f'https://anioracle.online/{page}'
    if '<meta name="description"' not in html:
        html = html.replace('</title>', f'</title>\n<meta name="description" content="{escape(description)}">', 1)
    if '<meta name="robots"' not in html:
        html = html.replace('</title>', '</title>\n<meta name="robots" content="index,follow,max-image-preview:large">', 1)
    if 'rel="canonical"' not in html:
        html = html.replace('</title>', f'</title>\n<link rel="canonical" href="{canonical}">', 1)
    if 'property="og:title"' not in html:
        title_match = re.search(r'<title>(.*?)</title>', html, re.S)
        title = title_match.group(1).strip() if title_match else page
        html = html.replace('</title>', f'</title>\n<meta property="og:title" content="{escape(title)}">\n<meta property="og:description" content="{escape(description)}">\n<meta property="og:url" content="{canonical}">\n<meta property="og:type" content="website">', 1)
    path.write_text(html, encoding='utf-8')

# Sitemap every public page, including legal/contact pages so the complete site is discoverable.
urls = ['https://anioracle.online/'] + [f'https://anioracle.online/{name}' for name in sorted(desc)]
lastmod = '2026-09-09'
entries = '\n'.join(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>weekly</changefreq><priority>{"1.0" if url.endswith("/") else "0.6"}</priority></url>' for url in urls)
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + '\n</urlset>\n', encoding='utf-8')

print('Patched index.html, public page metadata, and sitemap.xml')

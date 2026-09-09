from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
index = root / "index.html"
text = index.read_text()

old_css = '''.splash-video {
  position: absolute; inset: 0; z-index: 0;
  width: 100%; height: 100%;
  object-fit: contain;
  background: #ffffff;
}'''
new_css = '''.splash-video {
  position: absolute; inset: 0; z-index: 0;
  width: 100%; height: 100%;
  object-fit: contain;
  background: #ffffff;
}
.splash-poster {
  position: absolute; inset: 0; z-index: 0;
  width: 100%; height: 100%;
  object-fit: contain;
  background: #fff;
  animation: splash-poster-in 1.2s var(--ease-out-expo) both;
}
.splash-3d-logo {
  position: relative; z-index: 4;
  width: min(52vw, 270px); height: min(52vw, 270px);
  object-fit: contain;
  filter: drop-shadow(0 24px 24px rgba(40, 20, 75, .22));
  animation: splash-logo-float 3.2s ease-in-out .8s infinite, splash-logo-in .9s var(--ease-out-expo) .15s both;
  transform-origin: center;
}
@keyframes splash-poster-in { from { opacity: 0; transform: scale(1.035); } to { opacity: 1; transform: scale(1); } }
@keyframes splash-logo-float { 0%,100% { transform: translateY(0) rotate(-1deg); } 50% { transform: translateY(-8px) rotate(1deg); } }
@media (prefers-reduced-motion: reduce) {
  .splash-poster, .splash-3d-logo, .splash-logo { animation: none !important; }
}'''
if old_css not in text:
    raise SystemExit("splash CSS anchor not found")
text = text.replace(old_css, new_css, 1)

old_markup = '''<div id="splash">
  <video class="splash-video" id="splash-video" muted playsinline preload="auto" autoplay>
    <source src="https://res.cloudinary.com/de6izpjix/video/upload/q_auto,f_auto/Untitled_design_v7zevb.mp4" type="video/mp4">
  </video>
  <!-- Top-left Ribons brand -->'''
new_markup = '''<div id="splash" aria-label="AniOracle intro">
  <img class="splash-poster" src="./assets/anioracle-splash.png" alt="AniOracle logo artwork">
  <img class="splash-3d-logo" src="./assets/anioracle-logo-3d.png" alt="AniOracle 3D logo">
  <!-- Top-left Ribons brand -->'''
if old_markup not in text:
    raise SystemExit("splash markup anchor not found")
text = text.replace(old_markup, new_markup, 1)

old_js = '''  const splashVideo = document.getElementById('splash-video');
  if (splashVideo) {
    // Play video immediately as the intro animation
    splashVideo.play().catch(() => {});
    // Dismiss when video ends
    splashVideo.addEventListener('ended', dismissSplash);
    // Fallback: dismiss after 5s in case video doesn't load/end
    setTimeout(dismissSplash, 5000);
  } else {
    setTimeout(dismissSplash, 5000);
  }'''
new_js = '''  // The intro is intentionally local and media-light: it works without a CDN,
  // respects reduced-motion preferences, and never blocks the main app.
  const delay = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 650 : 2600;
  setTimeout(dismissSplash, delay);'''
if old_js not in text:
    raise SystemExit("splash JS anchor not found")
text = text.replace(old_js, new_js, 1)

# Keep the existing canonical if present, otherwise add one after viewport.
if 'rel="canonical"' in text:
    text = re.sub(r'<link rel="canonical" href="[^"]+"\s*/?>', '<link rel="canonical" href="https://anioracle.online/">', text, count=1)
else:
    text = text.replace('<meta name="viewport"', '<link rel="canonical" href="https://anioracle.online/">\n<meta name="viewport"', 1)

index.write_text(text)

(root / "robots.txt").write_text('''User-agent: *\nAllow: /\n\n# Allow major search and answer-engine crawlers to discover public AniOracle pages.\nUser-agent: GPTBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://anioracle.online/sitemap.xml\n''')

sitemap = root / "sitemap.xml"
sitemap.write_text(sitemap.read_text().replace('https://anioracle.com/', 'https://anioracle.online/').replace('https://anioracle.com/', 'https://anioracle.online/'))

(root / "llms.txt").write_text('''# AniOracle\n\n> AniOracle is a fan-made anime discovery and entertainment site covering characters, power levels, versus battles, manga, seasonal anime, and AI-assisted exploration.\n\n## Primary sections\n\n- [Home](https://anioracle.online/) — featured anime, trending characters, and discovery tools.\n- [Anime Wiki](https://anioracle.online/wiki.html) — anime and character reference content.\n\n## Editorial and rights note\n\nAniOracle is non-commercial and fan-made. Anime titles, character names, images, and related content belong to their respective creators and rights holders.\n''')

print("Updated intro, canonical URL, robots.txt, sitemap.xml, and llms.txt")

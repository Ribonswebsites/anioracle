from pathlib import Path
import re

root=Path('/home/ubuntu/anioracle')

# Homepage: add Fashion Week card and remove the adult body-measurement search phrase.
p=root/'index.html'
s=p.read_text(encoding='utf-8')
old='''    <a href="./most-beautiful-v2-2.html" class="ao-seo-card"><strong>Most Beautiful Anime Characters</strong><span>Fan rankings and visual profiles across popular anime universes.</span></a>'''
new=old+'''\n    <a href="./anime-fashion-week.html" class="ao-seo-card"><strong>Anime Fashion Week</strong><span>Top 20 anime character outfits, four fashion skills, category ratings, and runway awards.</span></a>'''
if old in s and 'Anime Fashion Week</strong>' not in s:
    s=s.replace(old,new)
s=s.replace('<span>One Piece bust size revealed by Oda</span>','<span>One Piece Oda SBS facts</span>')
# Splash only once per browser session; internal returns do not replay intro.
s=s.replace("function initSplash() {\n  function dismissSplash() {", "function initSplash() {\n  const splashSeen = sessionStorage.getItem('anioracle_splash_seen') === '1';\n  function dismissSplash() {")
s=s.replace("    if (!splashEl || splashEl.style.display === 'none') return;", "    if (!splashEl || splashEl.style.display === 'none') return;\n    sessionStorage.setItem('anioracle_splash_seen','1');")
s=s.replace("  const delay = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 650 : 2600;\n  setTimeout(dismissSplash, delay);", "  if (splashSeen) { splashEl.style.display = 'none'; return; }\n  const delay = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 650 : 2600;\n  setTimeout(dismissSplash, delay);")
p.write_text(s,encoding='utf-8')

# Most Beautiful: remove adult-coded characters from the general-audience ranking and use browser history.
p=root/'most-beautiful-v2-2.html'
s=p.read_text(encoding='utf-8')
s=s.replace("<button class=\"hero-back\" onclick=\"window.location.href='index.html'\">", "<button class=\"hero-back\" onclick=\"returnToAniOracle()\">")
s=s.replace("const list1 = document.getElementById('card-list');\nconst top20 = CHARS.filter(c=>c.rank<=20).map(buildCard).join('');", "const SAFE_CHARS = CHARS.filter(c => !['Rias Gremory','Akeno Himejima','Darkness (Lalatina)','Android 18'].includes(c.name)).map((c,i) => ({...c, rank:i+1}));\nconst list1 = document.getElementById('card-list');\nconst top20 = SAFE_CHARS.filter(c=>c.rank<=20).map(buildCard).join('');")
s=s.replace("const bottom10 = CHARS.filter(c=>c.rank>20).map(buildCard).join('');", "const bottom10 = SAFE_CHARS.filter(c=>c.rank>20).map(buildCard).join('');")
marker='</body>'
back='''<script>function returnToAniOracle(){try{sessionStorage.setItem('anioracle_return_page','home');}catch(e){} if (history.length>1 && document.referrer.includes(location.origin)) history.back(); else location.href='index.html';}</script>'''
if 'function returnToAniOracle' not in s:
    s=s.replace(marker,back+marker)
p.write_text(s,encoding='utf-8')

# Replace the adult-oriented hidden fact dataset with fashion/design facts.
p=root/'index.html'
s=p.read_text(encoding='utf-8')
start=s.find('// ── CHEST & WAIST DATA ──')
end=s.find('// Rebuild all', start)
if start!=-1 and end!=-1:
    replacement='''// ── CHARACTER DESIGN & FASHION FACTS ──\nDYK_DATA.design = [\n  {q:"Why do anime outfits matter to character design?", a:"Silhouette, color, and accessories communicate role, personality, and world-building before a character speaks."},\n  {q:"What are AniOracle fashion skills?", a:"Silhouette control, color harmony, accessory styling, and character-world coherence."},\n  {q:"Where can I compare anime outfits?", a:"Visit Anime Fashion Week for the top 20 editorial outfit rankings and category awards."},\n];\n\n'''
    s=s[:start]+replacement+s[end:]
# Replace remaining explicit adult search-copy lines with safe design language.
s=s.replace("answer:\"Boa Hancock has the largest chest measurements of any woman in the entire One Piece universe — and one of the largest in all of anime\", detail:\"In SBS Vol.53, Oda officially released Hancock's measurements: B111 / W61 / H91 cm. Nami is B98/W58/H90 and Robin is B99/W59/H89. Hancock's chest is 111cm — the largest Oda has ever drawn for a female character. Fans calculated this makes Hancock's silhouette physically extraordinary even by manga standards.\"", "answer:\"Boa Hancock has one of One Piece's most recognizable character designs\", detail:\"Her royal silhouette, cape, color palette, and accessories create a strong visual identity.\"")
s=s.replace('What are Boa Hancock\'s official measurements?','What makes Boa Hancock\'s character design distinctive?')
s=s.replace("answer:\"B:111 / W:61 / H:91 cm — the largest chest measurements Oda has ever given a character\", detail:\"Oda stated these in SBS Vol.53. For reference: Nami is B:98/W:58/H:90, Robin is B:99/W:59/H:89, and Nojiko is B:95/W:55/H:85. Hancock's chest at 111cm is significantly larger than any other female character Oda has officially measured.\"", "answer:\"Royal silhouette, bold palette, and instantly recognizable accessories\", detail:\"AniOracle focuses on character design language rather than body measurements.\"")
p.write_text(s,encoding='utf-8')
print('integration patched')
''

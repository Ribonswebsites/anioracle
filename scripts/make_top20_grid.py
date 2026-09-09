from pathlib import Path
import re
p=Path('/home/ubuntu/anioracle/anime-fashion-week.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\(function\(\)\{\s*var frames=\[\].*?\}\)\(\);\s*', '', s, count=1, flags=re.S)
p.write_text(s,encoding='utf-8')
css=Path('/home/ubuntu/anioracle/editorial-pages.css')
c=css.read_text(encoding='utf-8')
start=c.find('/* Fashion Week Top 20:')
if start<0: raise SystemExit('top20 css not found')
c=c[:start]+'''/* Fashion Week Top 20: four uploaded images displayed as a fixed AniOracle-style grid. */
#rankings{position:relative;isolation:isolate;overflow:hidden;background:linear-gradient(180deg,rgba(5,3,13,.88),rgba(5,3,13,.97))}.ranking-bg{position:absolute;z-index:-1;inset:0;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:2px;overflow:hidden;pointer-events:none}.ranking-bg div{position:relative;background-position:center;background-size:cover;opacity:.62;transform:scale(1.04)}.ranking-bg div:after{content:"";position:absolute;inset:0;background:rgba(5,3,13,.62)}
'''
css.write_text(c,encoding='utf-8')
print('converted Top 20 to fixed four-panel grid')

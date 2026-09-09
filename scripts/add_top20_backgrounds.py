from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-fashion-week.html')
s=p.read_text(encoding='utf-8')
needle='<section class="section" id="rankings">'
insert='<section class="section" id="rankings"><div class="ranking-bg" aria-hidden="true"><div style="background-image:url(\'1788934050686.png\')"></div><div style="background-image:url(\'1788934054076.png\')"></div><div style="background-image:url(\'1788934057568.png\')"></div><div style="background-image:url(\'1788934064190.png\')"></div></div>'
if needle not in s: raise SystemExit('rankings section not found')
p.write_text(s.replace(needle,insert,1),encoding='utf-8')
print('added four Top 20 background frames')

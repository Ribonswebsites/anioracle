from pathlib import Path
root=Path('/home/ubuntu/anioracle')
changes={
'anime-fashion-week.html':('<h1>Anime<br>Fashion Week</h1>','<h1 class="original-hero-title"><span class="hero-plain">Anime</span><span class="hero-grad">Fashion Week</span><span class="hero-stroke">RIBONS ORIGINAL</span></h1>'),
'anime-games.html':('<h1>Anime<br>Games</h1>','<h1 class="original-hero-title"><span class="hero-plain">Anime</span><span class="hero-grad">Games</span><span class="hero-stroke">RIBONS ORIGINAL</span></h1>')}
for name,(old,new) in changes.items():
 p=root/name;s=p.read_text(encoding='utf-8')
 if old not in s: raise SystemExit(f'heading not found in {name}')
 p.write_text(s.replace(old,new,1),encoding='utf-8')
print('updated Ribons Originals hero headings')

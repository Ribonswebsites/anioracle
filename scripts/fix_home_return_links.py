from pathlib import Path
root=Path('/home/ubuntu/anioracle')
p=root/'index.html'
s=p.read_text(encoding='utf-8').replace("window.location='most-beautiful-v2-2.html'", "window.location='index.html#home-most-beautiful'")
p.write_text(s,encoding='utf-8')
for name, old, new in [
 ('anime-fashion-week.html','href="index.html"','href="index.html#home-anime-fashion-week"'),
 ('anime-games.html','href="index.html"','href="index.html#home-anime-games"'),
 ('most-beautiful-v2-2.html',"location.href='index.html'","location.href='index.html#home-most-beautiful'"),
]:
 p=root/name; s=p.read_text(encoding='utf-8'); s=s.replace(old,new); p.write_text(s,encoding='utf-8')
print('home return links fixed')

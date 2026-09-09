from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-games.html')
s=p.read_text(encoding='utf-8').replace("url('hero-promo.mp4')","url('hero-opm.jpg')")
p.write_text(s,encoding='utf-8')
print('games hero asset fixed')

from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-games.html')
s=p.read_text(encoding='utf-8').replace("x.hidden=f!=='all'&&x.dataset.p!==f)}function openGame", "x.hidden=f!=='all'&&x.dataset.p!==f)};function openGame")
p.write_text(s,encoding='utf-8')
print('repaired games filter handler')

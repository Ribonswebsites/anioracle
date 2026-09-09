from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-games.html')
s=p.read_text(encoding='utf-8')
s=s.replace("x.hidden=f!=='all'&&x.dataset.platform!==f)});let n=0", "x.hidden=f!=='all'&&x.dataset.platform!==f)};let n=0")
p.write_text(s,encoding='utf-8')
print('games syntax fixed')

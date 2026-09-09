from pathlib import Path
root=Path('/home/ubuntu/anioracle')
for name, anchor in [('anime-fashion-week.html','home-anime-fashion-week'),('anime-games.html','home-anime-games')]:
    p=root/name
    s=p.read_text(encoding='utf-8')
    old=f'<a class="back" href="index.html#{anchor}">← Back to Home</a>'
    new=f'<a class="back" href="index.html#{anchor}" aria-label="Back to AniOracle home"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"></path><path d="m12 19-7-7 7-7"></path></svg><span>Home</span></a>'
    if old not in s: raise SystemExit(f'back control not found in {name}')
    p.write_text(s.replace(old,new,1),encoding='utf-8')
print('controls updated')

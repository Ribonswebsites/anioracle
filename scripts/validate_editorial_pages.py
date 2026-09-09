from pathlib import Path
from html.parser import HTMLParser
import re, subprocess, tempfile
for name in ('anime-fashion-week.html','anime-games.html'):
    p=Path('/home/ubuntu/anioracle')/name
    text=p.read_text(encoding='utf-8')
    HTMLParser().feed(text)
    blocks=re.findall(r'<script>(.*?)</script>', text, re.S)
    js=Path('/tmp/'+name+'.js'); js.write_text('\n'.join(blocks),encoding='utf-8')
    result=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
    if result.returncode: raise SystemExit(result.stderr)
    print(name,'ok',p.stat().st_size,'bytes',len(blocks),'script blocks')

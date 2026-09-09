from pathlib import Path
import re

html = Path('index.html').read_text(encoding='utf-8')
blocks = []
for match in re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.S | re.I):
    tag = match.group(0).split('>', 1)[0].lower()
    if 'application/ld+json' not in tag and 'application/json' not in tag:
        blocks.append(match.group(1))
Path('/tmp/anioracle-executable.js').write_text('\n'.join(blocks), encoding='utf-8')
print(f'executable script blocks: {len(blocks)}')
print(f'bytes: {Path("/tmp/anioracle-executable.js").stat().st_size}')

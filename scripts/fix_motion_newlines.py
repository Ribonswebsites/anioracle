from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = s.index('\\n/* ══ SCROLL MOTION + RIGHTWARD STRIP LOOP ══ */')
end_marker = '/* ══════════════════════════════════\n   NAV\n══════════════════════════════════ */'
end = s.index(end_marker, start)
block = s[start:end]
block = block.replace('\\n', '\n')
s = s[:start] + block + s[end:]
p.write_text(s, encoding='utf-8')
print('Fixed escaped newlines in motion controller')

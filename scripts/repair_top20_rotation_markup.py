from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-fashion-week.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<script>\n(function(){\n  var frames=[].slice.call(document.querySelectorAll(\'#rankings .ranking-bg div\'));', "(function(){\n  var frames=[].slice.call(document.querySelectorAll('#rankings .ranking-bg div'));")
s=s.replace("})();\n</script></script></body></html>", "})();\n</script></body></html>")
p.write_text(s,encoding='utf-8')
print('repaired nested rotation script')

from pathlib import Path
import re
p=Path('/home/ubuntu/anioracle/most-beautiful-v2-2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'<!-- ══ 18\+ AGE GATE ══ -->.*?(?=</style>)','',s,flags=re.S)
s=re.sub(r'<div id="age-gate">.*?</script>\s*','',s,flags=re.S)
s=s.replace('Most Beautiful Characters — AniOracle','Most Beautiful Anime Character Designs — AniOracle')
s=s.replace('Browse AniOracle fan rankings of the most beautiful anime characters from popular anime universes.','Browse AniOracle all-ages rankings of anime character design, visual style, costume language, and iconic looks.')
p.write_text(s,encoding='utf-8')
print('removed Most Beautiful age gate')

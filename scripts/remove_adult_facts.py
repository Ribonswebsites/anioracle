from pathlib import Path
p=Path('/home/ubuntu/anioracle/index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("  const isBodyQ = q.includes('chest') || q.includes('breast') || q.includes('boob') || q.includes('bust') || q.includes('biggest') || q.includes('largest') || q.includes('most') || q.includes('top') || q.includes('ranking') || q.includes('list') || q.includes('rank');", "  const isBodyQ = q.includes('fashion') || q.includes('outfit') || q.includes('style') || q.includes('design') || q.includes('ranking') || q.includes('list') || q.includes('rank');")
s=s.replace("  if (isBodyQ && (q.includes('chest') || q.includes('breast') || q.includes('boob') || q.includes('bust'))) {", "  if (q.includes('fashion') || q.includes('outfit') || q.includes('style') || q.includes('design')) { return 'Try Anime Fashion Week for outfit categories, color palettes, silhouette notes, accessory styling, and four repeatable fashion skills for every featured character.'; }")
s=s.replace("  if (isBodyQ && (q.includes('ass') || q.includes('butt') || q.includes('hip'))) {", "  if (false) {")
p.write_text(s,encoding='utf-8')
print('safe search branch installed')

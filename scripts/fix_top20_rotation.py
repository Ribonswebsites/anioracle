from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-fashion-week.html')
s=p.read_text(encoding='utf-8')
marker='</script></body></html>'
addition="""<script>
(function(){
  var frames=[].slice.call(document.querySelectorAll('#rankings .ranking-bg div'));
  if(!frames.length)return;
  var i=0;
  frames[0].classList.add('active');
  setInterval(function(){
    frames[i].classList.remove('active');
    i=(i+1)%frames.length;
    frames[i].classList.add('active');
  },4200);
})();
</script>"""
if marker not in s: raise SystemExit('page marker not found')
s=s.replace(marker,addition+marker,1)
p.write_text(s,encoding='utf-8')
print('added timed Top 20 rotation')

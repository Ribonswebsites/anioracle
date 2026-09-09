from pathlib import Path
p=Path('/home/ubuntu/anioracle/anime-fashion-week.html')
s=p.read_text(encoding='utf-8')
s=s.replace("function filters(id,key){document.querySelector(id).onclick=e=>{if(e.target.tagName!=='BUTTON')return;document.querySelectorAll(id+' button').forEach(b=>b.classList.remove('on'));e.target.classList.add('on');let f=e.target.dataset.f;document.querySelectorAll(key).forEach(x=>x.hidden=f!=='all'&&x.dataset[key.slice(4)]!==f)}}filters('#gender','[data-g]');filters('#category','#grid [data-c]');", "function filters(id,key,prop){document.querySelector(id).onclick=e=>{if(e.target.tagName!=='BUTTON')return;document.querySelectorAll(id+' button').forEach(b=>b.classList.remove('on'));e.target.classList.add('on');let f=e.target.dataset.f;document.querySelectorAll(key).forEach(x=>x.hidden=f!=='all'&&x.dataset[prop]!==f)}}filters('#gender','[data-g]','g');filters('#category','#grid [data-c]','c');")
p.write_text(s,encoding='utf-8')
print('fashion filters fixed')

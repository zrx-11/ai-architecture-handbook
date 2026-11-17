#!/usr/bin/env python3
"""把 _build/deep_courses/<slug>/content.html 组装成统一风格的单文件深潜课。"""
from pathlib import Path
import json, re, html

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_build' / 'deep_courses'

CSS = r"""
:root{
  --bg:#0f1117;--bg2:#161922;--bg3:#1e2230;--panel:#1a1e2a;
  --text:#e4e6ed;--muted:#9ba1b3;--dim:#6b7184;
  --accent:#7c5bff;--accent2:#5b9dff;--green:#38d39f;--warn:#f5a623;
  --border:#2a3040;--soft:rgba(124,91,255,.10);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;overflow-x:hidden;max-width:100vw}
body{font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.78;font-size:15.5px;overflow-x:hidden;
  overflow-wrap:break-word;word-break:break-word}
a{color:var(--accent2);text-decoration:none}
a:hover{text-decoration:underline}
.progress{position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:999;width:0}
.topbar{position:fixed;top:3px;left:0;right:0;height:54px;background:rgba(15,17,23,.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--border);z-index:900;
  display:flex;align-items:center;gap:12px;padding:0 18px}
.topbar button{display:none;background:var(--bg3);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:7px 10px;font-size:17px;cursor:pointer}
.brand{font-weight:700;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.brand span{color:var(--muted);font-weight:400;margin-left:8px}
.topbar .back{margin-left:auto;font-size:12.5px;color:var(--muted);border:1px solid var(--border);
  padding:5px 9px;border-radius:999px;white-space:nowrap}
.sidebar{position:fixed;top:57px;left:0;bottom:0;width:250px;background:var(--bg2);
  border-right:1px solid var(--border);overflow-y:auto;padding:18px 0;z-index:800;
  transition:transform .25s}
.sidebar h2{font-size:12px;color:var(--dim);font-weight:600;letter-spacing:.08em;
  padding:0 20px 10px;text-transform:uppercase}
.nav-item{display:block;padding:9px 20px;font-size:13px;color:var(--muted);
  border-left:3px solid transparent;cursor:pointer;line-height:1.45}
.nav-item:hover{background:var(--bg3);color:var(--text);text-decoration:none}
.nav-item.active{border-left-color:var(--accent);color:var(--text);background:var(--bg3)}
.nav-item small{display:block;color:var(--dim);font-size:11px;margin-top:1px}
.main{margin-left:250px;padding:80px 28px 60px;max-width:1180px}
.wrap{max-width:860px;margin:0 auto}
section{padding:4px 0 30px;border-bottom:1px solid rgba(42,48,64,.55);margin-bottom:26px;scroll-margin-top:70px}
section:last-of-type{border-bottom:0}
h2{font-size:clamp(1.35rem,3vw,1.85rem);line-height:1.28;margin:8px 0 14px;letter-spacing:-.01em}
h2 .num{color:var(--accent);font-size:.78em;margin-right:9px;font-variant-numeric:tabular-nums}
h3{font-size:1.05rem;margin:18px 0 7px;color:var(--text)}
h4{font-size:.96rem;margin:14px 0 5px;color:var(--muted)}
p{margin:9px 0}
ul,ol{margin:8px 0 10px 1.35em}
li{margin:4px 0}
strong{color:#fff;font-weight:650}
code{font-family:"SFMono-Regular",Consolas,monospace;background:var(--bg3);
  padding:1px 5px;border-radius:4px;font-size:.9em;color:#c9d5ff}
pre{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px;
  overflow-x:auto;font-size:13px;line-height:1.55;margin:12px 0}
pre code{background:none;padding:0;color:#d8def0}
.formula{background:var(--panel);border:1px solid var(--border);border-left:3px solid var(--accent);
  border-radius:8px;padding:10px 14px;margin:12px 0;overflow-x:auto;font-size:1.02em}
.formula .katex-display{margin:0}
table{width:100%;border-collapse:collapse;margin:13px 0;font-size:13.5px;display:block;overflow-x:auto}
th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--bg3);color:#fff;font-weight:600;white-space:nowrap}
td{color:var(--text)}
table th:first-child,table td:first-child{white-space:nowrap}
.note{background:rgba(91,157,255,.07);border:1px solid rgba(91,157,255,.35);border-radius:8px;
  padding:10px 13px;margin:12px 0;font-size:14px;color:#c9d8f5}
.warn{background:rgba(245,166,35,.07);border:1px solid rgba(245,166,35,.35);border-radius:8px;
  padding:10px 13px;margin:12px 0;font-size:14px;color:#f3d19a}
.good{background:rgba(56,211,159,.07);border:1px solid rgba(56,211,159,.35);border-radius:8px;
  padding:10px 13px;margin:12px 0;font-size:14px;color:#b5f0d9}
details{border:1px solid var(--border);border-radius:9px;margin:12px 0;background:var(--bg2)}
details summary{cursor:pointer;padding:10px 13px;font-size:13.5px;color:var(--accent2);font-weight:600}
details .inner{padding:2px 14px 14px;border-top:1px solid var(--border)}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:14px 0}
.flow .box{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:7px 11px;
  font-size:13px;text-align:center;min-width:74px}
.flow .arrow{color:var(--dim);font-size:18px}
.quiz{border:1px solid var(--border);border-radius:11px;padding:14px;margin:14px 0;background:var(--bg2)}
.quiz .q{font-weight:600;color:#fff;margin:0 0 9px;font-size:14.5px}
.quiz .opt{display:block;width:100%;text-align:left;background:var(--bg);color:var(--text);
  border:1px solid var(--border);border-radius:8px;padding:9px 11px;margin:6px 0;font:inherit;
  font-size:13.5px;cursor:pointer;line-height:1.5}
.quiz .opt:hover{border-color:var(--accent)}
.quiz .opt.ok{border-color:var(--green);background:rgba(56,211,159,.1)}
.quiz .opt.bad{border-color:#ff6b6b;background:rgba(255,107,107,.1)}
.quiz .fb{display:none;margin-top:9px;font-size:13.5px;line-height:1.65;color:var(--muted);border-top:1px dashed var(--border);padding-top:9px}
.quiz .fb.show{display:block}
.quiz .fb b{color:var(--text)}
.pager{display:flex;justify-content:space-between;gap:10px;margin:18px 0 8px}
.pager button{background:var(--bg3);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:9px 14px;font:inherit;font-size:13px;cursor:pointer}
.pager button:hover{border-color:var(--accent)}
.foot{color:var(--dim);font-size:12.5px;margin-top:24px;line-height:1.7}
.katex-fallback{background:rgba(245,166,35,.07);border:1px solid rgba(245,166,35,.35);
  border-radius:8px;padding:9px 12px;margin:10px 0;color:#f3d19a;font-size:13px;display:none}
@media(max-width:900px){
  .topbar button{display:block}
  .brand span{display:none}
  .sidebar{transform:translateX(-100%);top:57px;width:82vw;max-width:310px;box-shadow:20px 0 40px rgba(0,0,0,.35)}
  .sidebar.open{transform:translateX(0)}
  .main{margin-left:0;padding:76px 16px 48px}
  h2{font-size:1.3rem}
  .formula{padding:8px 10px}
  .formula .katex{font-size:.86em}
  table{font-size:12px}
  .flow{gap:5px}.flow .box{font-size:12px;padding:6px 8px;min-width:60px}.flow .arrow{font-size:14px}
}
@media(max-width:420px){
  body{font-size:15px}
  .main{padding-left:13px;padding-right:13px}
  .quiz .opt{font-size:13px}
}
"""

JS = r"""
const sections=[...document.querySelectorAll('section')];
const nav=[...document.querySelectorAll('.nav-item')];
const bar=document.querySelector('.progress');
const key='deep:'+location.pathname.split('/').filter(Boolean).slice(-2,-1)[0];
let cur=0;
function show(i,push){
  i=Math.max(0,Math.min(sections.length-1,i));
  sections.forEach((s,k)=>s.style.display=(k===i?'block':'none'));
  nav.forEach((n,k)=>n.classList.toggle('active',k===i));
  cur=i;
  bar.style.width=((i+1)/sections.length*100)+'%';
  try{localStorage.setItem(key,String(i))}catch(e){}
  if(push) history.replaceState(null,'','#'+sections[i].id);
  window.scrollTo({top:0,behavior:'smooth'});
}
nav.forEach((n,i)=>n.addEventListener('click',()=>{show(i,true);document.querySelector('.sidebar').classList.remove('open')}));
document.querySelector('#menu').addEventListener('click',()=>document.querySelector('.sidebar').classList.toggle('open'));
document.addEventListener('click',e=>{if(e.target.closest('.sidebar')||e.target.closest('#menu'))return;document.querySelector('.sidebar').classList.remove('open')});
document.querySelector('#prev').addEventListener('click',()=>show(cur-1,true));
document.querySelector('#next').addEventListener('click',()=>show(cur+1,true));
try{const saved=localStorage.getItem(key);if(saved!==null)cur=+saved||0}catch(e){}
const hash=location.hash.slice(1);const hi=sections.findIndex(s=>s.id===hash);if(hi>=0)cur=hi;
show(cur,false);
setTimeout(()=>window.scrollTo({top:0,behavior:"auto"}),0);

document.querySelectorAll('.quiz').forEach(q=>{
  const opts=[...q.querySelectorAll('.opt')], ans=+q.dataset.answer, fb=q.querySelector('.fb');
  opts.forEach((o,i)=>o.addEventListener('click',()=>{
    opts.forEach(x=>x.classList.remove('ok','bad'));
    if(i===ans){o.classList.add('ok')}else{o.classList.add('bad');opts[ans].classList.add('ok')}
    fb.innerHTML=(i===ans?'<b>正确。</b> ':'<b>不对。</b> ')+(q.dataset.explain||'');
    fb.classList.add('show');
    if(window.renderMathInElement){
      try{renderMathInElement(fb,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});}catch(e){}
    }
  }));
});

function render(){
  if(!window.renderMathInElement){
    const el=document.querySelector('.katex-fallback'); if(el) el.style.display='block'; return;
  }
  try{
    renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});
  }catch(e){const el=document.querySelector('.katex-fallback'); if(el) el.style.display='block';}
}
window.addEventListener('load',render);
"""

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} · 深潜课</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%237c5bff'/><text x='50' y='68' font-size='44' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='bold'>DS</text></svg>">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>{{CSS}}</style>
</head>
<body>
<div class="progress"></div>
<header class="topbar">
  <button id="menu" aria-label="目录">☰</button>
  <div class="brand">{{TITLE}}<span>{{SUBTITLE}}</span></div>
  <a class="back" href="../index.html">返回主手册</a>
</header>
<aside class="sidebar">
  <h2>课程目录</h2>
  {{NAV}}
</aside>
<main class="main"><div class="wrap">
<div class="katex-fallback">公式需要联网加载 KaTeX。当前显示的是 LaTeX 源码，文字、表格、测验仍可用。</div>
{{CONTENT}}
<div class="pager"><button id="prev">← 上一节</button><button id="next">下一节 →</button></div>
<div class="foot">这套深潜课是独立单文件页，进度存在本机浏览器。公式用 KaTeX 渲染；离线时显示源码，不影响阅读正文。<br>
相关分册：<a href="../index.html">主学习手册</a> · <a href="../00-跨书总览/深潜专题.md">深潜专题</a></div>
</div></main>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>{{JS}}</script>
</body>
</html>
"""

def build_one(d):
    meta=json.loads((d/'meta.json').read_text(encoding='utf-8'))
    content=(d/'content.html').read_text(encoding='utf-8')
    items=re.findall(r'<section id="([^"]+)" data-title="([^"]+)"',content)
    nav='\n'.join(f'<a class="nav-item" data-target="{i}">{html.escape(t)}<small>{n:02d}</small></a>' for n,(i,t) in enumerate(items))
    out=(TPL.replace('{{TITLE}}',meta['title']).replace('{{SUBTITLE}}',meta.get('subtitle',''))
         .replace('{{CSS}}',CSS).replace('{{NAV}}',nav).replace('{{CONTENT}}',content).replace('{{JS}}',JS))
    p=ROOT/meta['slug']/'index.html'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(out,encoding='utf-8')
    print(f'{meta["slug"]}: {len(items)} 节, {len(out)/1024:.1f} KB')

def main():
    for d in sorted(SRC.iterdir()):
        if d.is_dir() and (d/'meta.json').exists():
            build_one(d)

if __name__=='__main__': main()

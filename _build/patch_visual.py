#!/usr/bin/env python3
"""把总入口从默认白底文档壳重构成「深潜档案」视觉层。

只改壳与样式，不动书稿数据：
- 替换整段 CSS
- 重写顶栏 / 侧栏骨架
- 首页 hero 改为左文案 + 右参数栈
- 主题默认深色，保留浅色切换
- 移动端侧栏改为抽屉
- 给正文加面包屑与单次入场
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
BACKUP = ROOT / '_build' / 'index_before_visual.html'
CSS = (ROOT / '_build' / 'visual.css').read_text(encoding='utf-8')

src = INDEX.read_text(encoding='utf-8')
if not BACKUP.exists():
    BACKUP.write_text(src, encoding='utf-8')

# ---------- 1. 整段 CSS ----------
src = re.sub(r'<style>.*?</style>', '<style>\n' + CSS + '\n</style>', src, count=1, flags=re.S)

# ---------- 2. html / body / favicon ----------
src = src.replace('<html lang="zh-CN">', '<html lang="zh-CN" data-theme="dark">', 1)
src = src.replace('<body>', '<body data-theme="dark">\n<script>try{document.body.dataset.theme=document.documentElement.dataset.theme||"dark";}catch(e){}</script>', 1)
src = src.replace(
    '<link rel="icon" href="data:,">',
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E%3Crect width=\'32\' height=\'32\' fill=\'%23080d1a\'/%3E%3Cpath d=\'M6 8h20M9 16h17M12 24h14\' stroke=\'%235c7cff\' stroke-width=\'4\' stroke-linecap=\'round\'/%3E%3C/svg%3E">',
    1,
)

# 主题预读：避免浅色用户刷新时闪回深色
if 'localStorage.getItem("zs-theme")' not in src:
    src = src.replace(
        '</style>',
        '</style>\n<script>try{var t=localStorage.getItem("zs-theme");if(t==="light"||t==="dark"){document.documentElement.dataset.theme=t;}}catch(e){}</script>',
        1,
    )

# ---------- 3. 顶栏与侧栏骨架 ----------
HEADER = '''<header>
  <button id="menu-btn" class="icon-btn menu-btn" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="nav">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
  </button>
  <a class="brand" href="#/cross/doc1" aria-label="返回学习总览">
    <span class="brand-mark" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="3.2" stroke-linecap="round">
        <path class="m1" d="M4 5.5h16"/>
        <path class="m2" d="M7 12h13"/>
        <path class="m3" d="M10 18.5h10"/>
      </svg>
    </span>
    <span class="brand-text">AI 架构学习系统<span class="brand-sub">DeepSeek 论文与架构 · 学习总手册</span></span>
  </a>
  <span class="tabs" id="tabs"></span>
  <span class="hdr-right">
    <label class="search-wrap" aria-label="全书搜索">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>
      <input id="q" type="search" placeholder="搜索概念、章节、术语" autocomplete="off">
    </label>
    <button id="progress-export" class="icon-btn" type="button" title="导出学习进度">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 3v11"/><path d="m7.5 10 4.5 4.5 4.5-4.5"/><path d="M5 20h14"/></svg>
      <span class="btn-label">导出</span>
    </button>
    <button id="progress-import" class="icon-btn" type="button" title="导入学习进度">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 20V9"/><path d="m7.5 13.5 4.5-4.5 4.5 4.5"/><path d="M5 4h14"/></svg>
      <span class="btn-label">导入</span>
    </button>
    <button id="theme-btn" class="icon-btn" type="button" title="切换浅色 / 深色">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M20 12.5A8 8 0 1 1 11.5 4a6.2 6.2 0 0 0 8.5 8.5Z"/></svg>
      <span class="btn-label">浅色</span>
    </button>
    <input type="file" id="progress-file" accept="application/json" hidden>
  </span>
</header>'''

src = re.sub(r'<header>.*?</header>', HEADER, src, count=1, flags=re.S)

LAYOUT = '''<div class="layout">
  <button id="nav-scrim" type="button" aria-label="关闭目录" hidden></button>
  <aside class="sidebar" id="sidebar">
    <button id="nav-close" class="icon-btn nav-close" type="button" aria-label="关闭目录">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m6 6 12 12M18 6 6 18"/></svg>
    </button>
    <div class="side-progress">
      <div class="progress-number" id="progress-pct">0<span>%</span></div>
      <div class="progress-label" id="progress-label">选择一本书开始</div>
      <div id="progress-bar" aria-hidden="true"><div id="progress-fill"></div></div>
    </div>
    <nav id="nav"></nav>
  </aside>
  <main class="main"><div id="view" class="page"></div></main>
</div>'''

src = re.sub(
    r'<div class="layout">.*?</div>\s*<script>',
    LAYOUT + '\n<script>',
    src,
    count=1,
    flags=re.S,
)

# ---------- 4. 首页 hero ----------
OLD_HERO_START = "    pre='<div class=\"hero\"><div class=\"hero-kicker\">"
OLD_HERO_END_TOKEN = "+'</div></details>';"
if OLD_HERO_START in src:
    start = src.index(OLD_HERO_START)
    end = src.index(OLD_HERO_END_TOKEN, start) + len(OLD_HERO_END_TOKEN)
else:
    start = end = None
    if '<div class="hero"><div class="hero-copy">' not in src:
        raise SystemExit('未找到首页 hero 旧标记，也不是已应用视觉的版本')
    print('· 首页 hero 已是新版，跳过替换')

NEW_HERO = r'''    pre='<div class="hero"><div class="hero-copy">'
      +'<h1>一条主线，按依赖走完</h1>'
      +'<p class="hero-lede">数学和代码接近零基础也能走。这份学习总手册用八步主线，每步一个主入口；卡住再从资料库补。</p>'
      +'<div class="hero-actions"><a class="btn-primary" href="14-math-deep/index.html">从数学基础开始</a><a class="btn-ghost" href="#/cross/doc7">看知识覆盖地图</a></div>'
      +'<div class="hero-stats"><span><b>7</b> 本分册</span><span><b>15</b> 套深潜课</span><span><b>164</b> 节单点推导</span><span><b>67</b> 章系统课</span></div></div>'
      +'<div class="hero-stack" aria-label="DeepSeek 模型总参数与激活参数对比">'
      +'<div class="stack-head"><span>总参数 / 每 token 激活</span><span>按总参数排序</span></div>'
      + `<div class="stack-row"><span class="stack-name">V4 Pro</span><span class="stack-bar"><i class="v4pro" style="--w:100%"></i><b style="--a:3.1%"></b></span><span class="stack-val">1.6T<small>49B</small></span></div>`
      + `<div class="stack-row"><span class="stack-name">V4.1</span><span class="stack-bar"><i class="v41" style="--w:47%"></i><b style="--a:2.1%"></b></span><span class="stack-val">748B<small>8–16B</small></span></div>`
      + `<div class="stack-row"><span class="stack-name">V3</span><span class="stack-bar"><i class="v3" style="--w:42%"></i><b style="--a:5.5%"></b></span><span class="stack-val">671B<small>37B</small></span></div>`
      + `<div class="stack-row"><span class="stack-name">V4 Flash</span><span class="stack-bar"><i class="v4flash" style="--w:18%"></i><b style="--a:4.6%"></b></span><span class="stack-val">284B<small>13B</small></span></div>`
      +'<p class="stack-foot">条宽按总参数比例；绿色段是每 token 激活占比。V4.1 的 8–16B 按 16B 上限画段。</p>'
      +'</div></div>'
      +'<div class="path-head"><div><h2>学习路径</h2><p>按顺序点。每步先读主入口，再用右侧标签补缺口。</p></div><span class="path-meta">7 步 · 约 16 周</span></div>'
      +'<div class="simple-path">'
      + steps.map(s=>`<div class="step-card"><div class="step-num">${s.n}</div><div><h3>${esc(s.t)}</h3><p>${esc(s.d)}</p><div class="step-links"><a class="primary" href="${encodeURI(s.p)}">${esc(s.pl)}</a>${s.x.map(x=>`<a href="${encodeURI(x[0])}">${esc(x[1])}</a>`).join('')}</div></div></div>`).join('')
      +'</div>'
      +'<details class="library"><summary><span>资料库</span><em>7 本分册 · 15 套深潜课 · 5 个专题</em></summary>'
      +'<p class="lib-note">主线卡住时按关键词回来查。分册负责广度、依赖顺序和诊断；深潜课负责单点推到底。</p>'
      +'<h3>分册</h3><div class="lib-grid">'
      + META.map(m=>`<a class="lib-item book-card" href="#/book/${m.key}/path"><b>${esc(m.title)}</b><span>${m.chapters} 章 · ${m.quizzes} 测验</span></a>`).join('')
      +'</div><h3>深潜课</h3><div class="lib-grid deep">'
      + deep.map(d=>`<a class="lib-item" href="${encodeURI(d[0]+'/index.html')}" target="_blank"><b>${esc(d[1])}</b><span>${esc(d[2])} · ${esc(d[3])}</span></a>`).join('')
      +'</div><h3>专题</h3><div class="lib-grid topics">'
      + `<a class="lib-item" href="#/cross/doc7"><b>知识覆盖地图</b><span>哪些节点覆盖了、哪些还是缺口</span></a>`
      + `<a class="lib-item" href="#/cross/doc4"><b>学习节点地图</b><span>依赖主线与 12 周推进表</span></a>`
      + `<a class="lib-item" href="#/cross/doc6"><b>深潜专题</b><span>15 套课怎么选、怎么配主线</span></a>`
      + `<a class="lib-item" href="#/cross/doc2"><b>跨书概念映射</b><span>同一概念在不同分册的讲法</span></a>`
      + `<a class="lib-item" href="#/cross/doc3"><b>综合检验</b><span>跨书任务与进阶路线</span></a>`
      +'</div></details>';'''
if start is not None:
    src = src[:start] + NEW_HERO + src[end:]

# ---------- 5. 主题按钮 ----------
OLD_THEME = '''/* ---------- 主题 ---------- */
const themeBtn=$('#theme-btn');
themeBtn.onclick=()=>{
  const d=document.body.dataset.theme==='dark';
  document.body.dataset.theme=d?'':'dark';
  themeBtn.textContent=d?'🌙 深色':'☀️ 浅色';
};'''
NEW_THEME = '''/* ---------- 主题 ---------- */
const themeBtn=$('#theme-btn');
function paintThemeBtn(){
  const light=document.documentElement.dataset.theme==='light';
  const label=themeBtn&&themeBtn.querySelector('.btn-label');
  if(label) label.textContent=light?'深色':'浅色';
  if(themeBtn) themeBtn.setAttribute('aria-label',light?'切换到深色主题':'切换到浅色主题');
}
if(themeBtn){
  themeBtn.onclick=()=>{
    const light=document.documentElement.dataset.theme==='light';
    const next=light?'dark':'light';
    document.documentElement.dataset.theme=next;
    document.body.dataset.theme=next;
    try{localStorage.setItem('zs-theme',next)}catch(e){}
    paintThemeBtn();
  };
  paintThemeBtn();
}'''
if OLD_THEME in src:
    src = src.replace(OLD_THEME, NEW_THEME, 1)
else:
    print('· 主题按钮已是新版，跳过')

# ---------- 6. 进度函数 ----------
OLD_PROGRESS = '''function updateProgress(pct,label){
  $('#progress-fill').style.width=pct+'%';
  $('#progress-label').textContent=label;
}'''
NEW_PROGRESS = '''function paintProgress(pct,label){
  const fill=$('#progress-fill');
  if(fill) fill.style.transform='scaleX('+(Math.max(0,Math.min(100,pct))/100)+')';
  const pctEl=$('#progress-pct');
  if(pctEl) pctEl.innerHTML=pct+'<span>%</span>';
  const labelEl=$('#progress-label');
  if(labelEl) labelEl.textContent=label;
}
function updateProgress(pct,label){ paintProgress(pct,label); }'''
if OLD_PROGRESS in src:
    src = src.replace(OLD_PROGRESS, NEW_PROGRESS, 1)
else:
    print('· 进度函数已是新版，跳过')

OLD_PROGRESS_BOOK = '''  const pct=chs?Math.round(done/chs*100):0;
  $('#progress-fill').style.width=pct+'%';
  $('#progress-label').textContent=`《${(META.find(x=>x.key===book)||{}).title||book}》 进度 ${pct}% · 已学 ${done}/${chs} 章`;
}'''
NEW_PROGRESS_BOOK = '''  const pct=chs?Math.round(done/chs*100):0;
  paintProgress(pct,`《${(META.find(x=>x.key===book)||{}).title||book}》 进度 ${pct}% · 已学 ${done}/${chs} 章`);
}'''
if OLD_PROGRESS_BOOK in src:
    src = src.replace(OLD_PROGRESS_BOOK, NEW_PROGRESS_BOOK, 1)
else:
    print('· 分册进度函数已是新版，跳过')

# ---------- 7. 面包屑 ----------
OLD_BOOK_VIEW = '''  $('#view').innerHTML=html;
  if(cur.page==='cards') initCards();'''
NEW_BOOK_VIEW = '''  const m=META.find(x=>x.key===cur.book);
  let pageLabel=cur.page;
  if(cur.page.startsWith('chapter/')){
    const c=(B.manifest.chapters||[]).find(x=>x.id===cur.page.slice(8));
    if(c) pageLabel=c.title;
  }else if(cur.page.startsWith('concept/')){
    const c=(B.manifest.concepts||[]).find(x=>x.id===cur.page.slice(8));
    if(c) pageLabel=c.title;
  }else if(cur.page.startsWith('quiz/')) pageLabel='测验';
  else if(cur.page==='path') pageLabel='学习路径';
  else if(cur.page==='cards') pageLabel='抽认卡';
  else if(cur.page==='glossary') pageLabel='术语表';
  else if(cur.page==='diagnosis') pageLabel='诊断测试';
  else if(cur.page==='patterns') pageLabel='模式库';
  else if(cur.page==='cheatsheet') pageLabel='速查表';
  const bookTitle=esc(m?m.title:cur.book);
  let crumb='<div class="crumb"><a href="#/cross/'+FIRST_DOC+'">总览</a><span class="sep">/</span><a href="#/book/'+cur.book+'/path">'+bookTitle+'</a>';
  if(cur.page!=='path') crumb+='<span class="sep">/</span><span class="current">'+esc(pageLabel)+'</span>';
  crumb+='</div>';
  $('#view').innerHTML=crumb+html;
  if(cur.page==='cards') initCards();'''
if OLD_BOOK_VIEW in src:
    src = src.replace(OLD_BOOK_VIEW, NEW_BOOK_VIEW, 1)
else:
    print('· 分册面包屑已是新版，跳过')

OLD_CROSS_VIEW = '''  v.innerHTML = pre + html;
  renderMermaid();'''
NEW_CROSS_VIEW = '''  const cm=CROSS_META.find(c=>c.key===docId);
  const crumb=docId===FIRST_DOC?'':'<div class="crumb"><a href="#/cross/'+FIRST_DOC+'">总览</a><span class="sep">/</span><span class="current">'+esc(cm?cm.label:docId)+'</span></div>';
  v.innerHTML = crumb + pre + html;
  renderMermaid();'''
if OLD_CROSS_VIEW in src:
    src = src.replace(OLD_CROSS_VIEW, NEW_CROSS_VIEW, 1)
else:
    print('· 总览面包屑已是新版，跳过')

# ---------- 8. 路由入场 ----------
OLD_ROUTE = '''  if(cur.book==='cross') renderCross(); else renderBook();
  window.scrollTo(0,0);'''
NEW_ROUTE = '''  if(cur.book==='cross') renderCross(); else renderBook();
  const v=$('#view');
  if(v){ v.classList.remove('enter'); void v.offsetWidth; v.classList.add('enter'); }
  window.scrollTo(0,0);'''
if OLD_ROUTE in src:
    src = src.replace(OLD_ROUTE, NEW_ROUTE, 1)
else:
    print('· 路由入场已是新版，跳过')

# ---------- 9. 移动端目录抽屉 ----------
OLD_MOBILE_NAV = '''(function(){
  const sb=document.querySelector('.sidebar'); if(!sb) return;
  const btn=document.createElement('button'); btn.id='nav-toggle'; btn.textContent='目录（点开选择章节）';
  btn.onclick=()=>sb.classList.toggle('open');
  sb.insertBefore(btn, sb.querySelector('#nav'));
  window.addEventListener('hashchange',()=>{ if(window.innerWidth<=820) sb.classList.remove('open'); });
})();'''
NEW_MOBILE_NAV = '''(function(){
  const sb=document.querySelector('.sidebar'); if(!sb) return;
  const menu=$('#menu-btn'), close=$('#nav-close'), scrim=$('#nav-scrim');
  const setOpen=open=>{
    sb.classList.toggle('open',open);
    if(menu) menu.setAttribute('aria-expanded',open?'true':'false');
    if(scrim) scrim.hidden=!open;
    document.body.classList.toggle('nav-open',open);
  };
  if(menu) menu.onclick=()=>setOpen(!sb.classList.contains('open'));
  if(close) close.onclick=()=>setOpen(false);
  if(scrim) scrim.onclick=()=>setOpen(false);
  window.addEventListener('hashchange',()=>{ if(window.innerWidth<=980) setOpen(false); });
  window.addEventListener('keydown',e=>{ if(e.key==='Escape') setOpen(false); });
})();'''
if OLD_MOBILE_NAV in src:
    src = src.replace(OLD_MOBILE_NAV, NEW_MOBILE_NAV, 1)
else:
    print('· 移动端目录已是新版，跳过')

NEW_RENDER_TABS = """function renderTabs(){
  const el = $('#tabs'); el.innerHTML='';
  const SHORT={cross:'总览','deepseek-foundations':'基础','deepseek-papers':'论文','deepseek-architecture':'架构','machine-learning':'机器学习','neural-networks':'神经网络','deep-learning-scratch':'深度学习','deepseek-family':'全谱'};
  TABS.forEach(t=>{
    const b=document.createElement('button');
    b.className='tab'+(cur.book===t.key?' active':'');
    b.textContent=SHORT[t.key]||t.label;
    b.title=t.label;
    b.onclick=()=>{ location.hash = t.key==='cross' ? '#/cross/'+FIRST_DOC : '#/book/'+t.key+'/path'; };
    el.appendChild(b);
  });
}"""
src, _ = re.subn(r'function renderTabs\(\)\{.*?\n\}', NEW_RENDER_TABS, src, count=1, flags=re.S)

# ---------- 10. 去掉可见 emoji ----------
for a,b in [
    ('📖 出处：','出处：'),
    ('🩺 诊断测试','诊断测试'),
    ('🕸 知识图谱','知识图谱'),
    ('⬅ 前置：','前置：'),
    ('📚 ',''),
]:
    src = src.replace(a,b)

INDEX.write_text(src, encoding='utf-8')
print(f'✓ 视觉层已应用到 {INDEX} ({len(src)/1024:.1f} KB)')

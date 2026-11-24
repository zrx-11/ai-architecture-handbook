#!/usr/bin/env python3
"""总入口排版优化层：只改样式与头部高度同步，不改路由、数据结构与内容。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

STYLE = r"""<style id="frontend-layout-tuning">
/* ===== 排版优化：更宽的阅读区、两栏路线、数据侧栏、紧凑头部 ===== */
html{--header-h:104px}
html,body{overflow-x:clip}
body{font-size:16px;line-height:1.72}

/* 头部：品牌与工具一行，书籍标签单独一行横滑 */
header{
  display:grid;
  grid-template-columns:minmax(0,1fr) auto;
  grid-template-areas:"brand tools" "tabs tabs";
  align-items:center;
  gap:7px 22px;
  padding:8px 24px!important;
}
header .brand{margin:0;grid-area:brand;font-size:18px;line-height:1.3}
header .brand span{display:block;margin:2px 0 0;font-size:11.5px;line-height:1.35}
header .tabs{
  grid-area:tabs;
  display:flex;
  flex-wrap:nowrap;
  gap:6px;
  min-width:0;
  max-width:100%;
  overflow-x:auto;
  overflow-y:hidden;
  padding-bottom:3px;
  scrollbar-width:thin;
  mask-image:linear-gradient(to right,#000 0,#000 calc(100% - 36px),transparent 100%);
  -webkit-mask-image:linear-gradient(to right,#000 0,#000 calc(100% - 36px),transparent 100%);
}
header .tabs .tab{flex:0 0 auto;padding:5px 13px;font-size:12.5px}
header .tabs::-webkit-scrollbar{height:4px}
header .tabs::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
header .hdr-right{grid-area:tools;float:none;margin:0;justify-content:flex-end}
header #q{width:230px;height:38px;margin:0!important;padding:0 12px;font-size:13px!important;line-height:36px}
header .hdr-right button,#theme-btn{
  height:38px;
  padding:0 14px;
  font-size:13px!important;
  line-height:1;
  white-space:nowrap;
}
header #progress-export,header #progress-import{padding:0 11px}
header #theme-btn{font-size:14px!important}

/* 主体：不再被 920px 的阅读宽度卡住，首页铺开、正文单独限宽 */
.layout{width:100%;min-height:calc(100vh - var(--header-h))}
.sidebar{top:var(--header-h);height:calc(100vh - var(--header-h));padding:18px 16px}
.main{
  flex:1 1 auto;
  width:auto;
  max-width:1100px;
  margin:0 auto;
  padding:36px clamp(28px,4vw,52px) 96px;
}
#view{max-width:none;width:100%}

/* 正文页：中文阅读的测量宽度与字号重新定标 */
#view.page{
  max-width:780px;
  margin:0 auto;
  font-size:16.5px;
  line-height:1.85;
}
#view.page:has(.hero){max-width:none;margin:0}
#view.page h1{
  font-size:32px;
  text-wrap:normal;
  overflow-wrap:anywhere;
  line-height:1.32;
  padding-bottom:14px;
  margin:0 0 22px;
  border-bottom:1px solid var(--border);
}
#view.page h2{font-size:24px;line-height:1.4;margin:34px 0 14px}
#view.page h3{font-size:19px;line-height:1.5;margin:26px 0 10px}
#view.page p{margin:0 0 16px}
#view.page li{margin:4px 0;line-height:1.8}
#view.page table{font-size:14.5px}
#view.page th,#view.page td{padding:8px 12px}

/* 侧栏：去掉全大写字母距，选中项用左侧色条 */
.sidebar .nav-sec{
  font-size:12px;
  letter-spacing:0;
  text-transform:none;
  font-weight:600;
  margin:16px 0 6px;
}
.sidebar .nav-item{
  padding:6px 10px;
  border-left:2px solid transparent;
  border-radius:4px;
  font-size:14px;
}
.sidebar .nav-item.active{border-left-color:var(--accent)}

/* 首页 hero：左边标题与说明，右边四条数据；不堆三张等权卡 */
#view .hero{
  display:grid;
  grid-template-columns:minmax(0,1fr) 230px;
  grid-template-areas:"kicker stats" "title stats" "lede stats";
  grid-template-rows:auto auto 1fr;
  column-gap:48px;
  align-items:start;
  padding:10px 0 24px;
  margin-bottom:26px;
  border-bottom:1px solid var(--border);
}
#view .hero-kicker{
  grid-area:kicker;
  margin:0 0 2px;
  font-size:12.5px;
  font-weight:600;
  letter-spacing:0;
  text-transform:none;
  color:var(--accent);
}
#view.page .hero h1{
  grid-area:title;
  max-width:720px;
  margin:6px 0 16px;
  font-size:clamp(38px,4vw,56px);
  line-height:1.12;
  text-wrap:balance;
  overflow-wrap:break-word;
  min-width:0;
}
#view.page .hero p{
  grid-area:lede;
  max-width:680px;
  margin:0;
  font-size:16.5px;
  line-height:1.85;
  color:var(--muted);
}
#view .hero-stats{
  grid-area:stats;
  display:grid;
  grid-template-columns:1fr;
  gap:0;
  align-self:start;
  margin-top:4px;
  padding-left:24px;
  border-left:1px solid var(--border);
}
#view .hero-stats span{
  display:flex;
  flex-direction:column;
  gap:2px;
  padding:11px 0 12px;
  border-top:1px solid var(--border);
  font-size:12.5px;
  line-height:1.4;
  color:var(--muted);
}
#view .hero-stats span:first-child{border-top:0;padding-top:0}
#view .hero-stats b{
  margin:0;
  font-family:var(--font-display);
  font-size:26px;
  line-height:1.15;
  font-weight:700;
  color:var(--text);
}

/* 学习路线：桌面两栏，序号与内容形成稳定网格 */
#view .path-head{margin:0 0 16px}
#view .path-head h2{font-size:24px;margin:0 0 6px}
#view .path-head p{font-size:14.5px;line-height:1.65;margin:0;color:var(--muted)}
#view .simple-path{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:14px;
  margin:0 0 30px;
}
#view .step-card{
  grid-template-columns:44px minmax(0,1fr);
  gap:14px;
  height:100%;
  padding:18px;
  border-radius:12px;
}
#view .step-card > div:last-child{
  display:flex;
  flex-direction:column;
  min-width:0;
  height:100%;
}
#view .step-num{font-size:24px;line-height:1.1;padding-top:2px}
#view .step-card h3{font-size:17px;line-height:1.4;margin:0 0 6px}
#view .step-card p{font-size:14.5px;line-height:1.75;margin:0 0 12px}
#view .step-links{margin-top:auto}
#view .step-links a{font-size:12.5px;padding:4px 9px;line-height:1.5}

/* 资料库：卡片更紧凑，入口层级更清楚 */
#view .library{margin-top:30px;padding-top:20px}
#view .library summary{
  display:flex;
  justify-content:space-between;
  align-items:baseline;
  gap:16px;
  padding:4px 0;
}
#view .library summary span{font-size:18px}
#view .library summary em{font-size:12.5px}
#view .lib-grid{grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
#view .lib-item{min-height:64px;padding:12px 14px;border-radius:8px}
#view .lib-item b{font-size:14px;line-height:1.45}
#view .lib-item span{font-size:12px;line-height:1.55}

/* 可访问性：焦点环立即出现，不依赖动画 */
a:focus-visible,button:focus-visible,input:focus-visible,summary:focus-visible{
  outline:2px solid var(--accent);
  outline-offset:2px;
}

@media (max-width:1180px){
  #view .simple-path{grid-template-columns:1fr}
  #view .hero{grid-template-columns:minmax(0,1fr) 210px;column-gap:32px}
}

@media (max-width:820px){
  html{--header-h:0px}
  header{
    grid-template-columns:1fr;
    grid-template-areas:"brand" "tabs" "tools";
    gap:8px;
    padding:10px 14px!important;
  }
  header .brand span{display:none}
  header .hdr-right{
    display:flex;
    flex-wrap:nowrap;
    gap:6px;
    width:100%;
    justify-content:stretch;
  }
  header #q{flex:1 1 auto;width:auto;min-width:0}
  header .hdr-right button,#theme-btn{
    flex:0 0 auto;
    width:auto;
    height:34px;
    padding:0 6px;
    font-size:11px!important;
  }
  header #q{font-size:12px!important;padding:0 9px}
  #view .hero-kicker{font-size:10.5px;line-height:1.5}
  .layout{min-height:0}
  .sidebar{position:static;height:auto;padding:10px 14px}
  .main{
    width:100%!important;
    max-width:100%!important;
    margin:0!important;
    min-width:0;
    padding:20px 16px 64px;
  }
  #view .hero{
    display:block;
    padding:6px 0 16px;
    margin-bottom:20px;
  }
  #view.page .hero h1{
    font-size:clamp(32px,9vw,42px);
    line-height:1.16;
    margin:6px 0 12px;
  }
  #view.page .hero p{font-size:16px;line-height:1.8}
  #view .hero-stats{
    grid-template-columns:repeat(2,minmax(0,1fr));
    column-gap:16px;
    margin-top:18px;
    padding:6px 0 0;
    border-left:0;
    border-top:1px solid var(--border);
  }
  #view .hero-stats span{padding:9px 0 10px}
  #view .hero-stats b{font-size:20px}
  #view .simple-path{grid-template-columns:1fr;gap:10px}
  #view .step-card{grid-template-columns:38px minmax(0,1fr);gap:10px;padding:14px}
  #view .step-card p{font-size:14px}
  #view.page{max-width:none}
  #view.page h1{font-size:25px;line-height:1.35;word-break:keep-all;overflow-wrap:anywhere}
  #view.page h2{font-size:22px}
  #view.page p,#view.page li{font-size:16.2px;line-height:1.8}
  #view .library{margin-top:24px}
  #view .lib-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  #view .lib-item{padding:10px 11px}
  #view.page ul{padding-left:1.2em}
}
@media(max-width:360px){
  header #q{flex:1 1 0!important;width:0!important;min-width:0!important}
  header .hdr-right button,#theme-btn{padding:0 4px!important;font-size:10px!important;height:32px}
}

@media (max-width:420px){
  #view .lib-grid{grid-template-columns:1fr}
  #view .hero-stats{column-gap:12px}
}
</style>"""

SCRIPT = r"""<script id="frontend-header-height">
(function(){
  const h=document.querySelector('header');
  if(!h)return;
  const set=()=>document.documentElement.style.setProperty('--header-h',h.getBoundingClientRect().height+'px');
  set();
  addEventListener('resize',set,{passive:true});
  if(window.ResizeObserver) new ResizeObserver(set).observe(h);
})();
</script>"""


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(r'<style id="frontend-layout-tuning">.*?</style>\n?', "", text, flags=re.S)
    text = re.sub(r'<script id="frontend-header-height">.*?</script>\n?', "", text, flags=re.S)
    if "</head>" not in text or "</body>" not in text:
        print("未找到 head/body 插入点")
        return 1
    text = text.replace("</head>", STYLE + "\n</head>", 1)
    text = text.replace("</body>", SCRIPT + "\n</body>", 1)
    INDEX.write_text(text, encoding="utf-8")
    print("✓ 已注入前端排版优化层")
    return 0


if __name__ == "__main__":
    sys.exit(main())

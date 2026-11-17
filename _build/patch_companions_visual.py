#!/usr/bin/env python3
"""给 7 本单书学习伴侣套一层与总入口一致的深色视觉。

只改壳，不动 DATA 里的书稿内容。默认深色，按钮可切回暖灰浅色。
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

DARK = '''[data-theme="dark"]{
  --bg:#080d1a; --panel:#101a2f; --text:#f1f5ff; --muted:#8494b4;
  --accent:#5c7cff; --accent-soft:#16213b; --border:#253252;
  --ok:#2bd9a5; --bad:#ff7088; --code-bg:#0b1222;
  --depth-bg:#141b30; --depth-border:#3a4c7a;
  --grid:rgba(199,208,229,.045);
}'''

LIGHT = ''':root{
  --bg:#edf1f8; --panel:#f9fbff; --text:#111827; --muted:#5b6478;
  --accent:#3950de; --accent-soft:#e4e9ff; --border:#d9e0ee;
  --ok:#0f9f74; --bad:#c62b45; --code-bg:#f2f4fa;
  --depth-bg:#fff7e0; --depth-border:#b8860b;
  --grid:rgba(17,24,39,.035);
  --font-display:"Noto Serif CJK SC","Noto Serif SC","Songti SC",STSong,Georgia,serif;
}'''

SKIN = '''<style id="visual-skin">
:root{--font-body:"Noto Sans CJK SC","Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;
  --font-mono:"JetBrains Mono","SFMono-Regular",Consolas,"Liberation Mono",monospace}
html,body{overflow-x:clip;max-width:100%}
body{font-family:var(--font-body);background-color:var(--bg);
  background-image:radial-gradient(circle at 1px 1px,var(--grid) 1px,transparent 0);background-size:26px 26px;
  color:var(--text);line-height:1.8;font-size:15.5px;-webkit-font-smoothing:antialiased}
a{color:var(--accent)}
::selection{background:var(--accent);color:#fff}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.sidebar{width:280px;padding:20px 18px;background:var(--panel);border-right:1px solid var(--border)}
.sidebar h1{font-family:var(--font-display);color:var(--text);font-size:1.15rem;line-height:1.42;font-weight:600;letter-spacing:-.01em;margin:0 0 6px}
.sidebar .sub{font-size:11.5px;line-height:1.65;color:var(--muted);margin-bottom:16px}
#q{height:38px;background:var(--code-bg);border:1px solid var(--border);border-radius:8px;font-size:14px;padding:0 10px;margin-bottom:14px}
#q::placeholder{color:var(--muted)}
.nav-sec{font-size:10.5px;letter-spacing:.1em;color:var(--muted);margin:18px 0 6px}
.nav-item{padding:7px 10px;border-radius:8px;font-size:13.5px;line-height:1.5;color:var(--text)}
.nav-item:hover{background:var(--accent-soft);text-decoration:none}
.nav-item.active{background:var(--accent-soft);color:var(--accent);font-weight:600;box-shadow:inset 3px 0 0 var(--accent)}
.main{padding:34px 44px 96px;max-width:940px}
.topbar{background:var(--bg);padding:0 0 14px;margin-bottom:24px;border-bottom:1px solid var(--border);gap:8px}
.topbar button{height:32px;padding:0 11px;border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:8px;font-size:12.5px;font-family:var(--font-body)}
.topbar button:hover{border-color:var(--accent);color:var(--accent)}
#progress-bar{height:4px;background:var(--border);border-radius:0;margin:10px 0 8px}
#progress-bar>div{background:var(--accent);transition:none}
.page h1{font-family:var(--font-display);color:var(--text);font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.42;font-weight:600;letter-spacing:-.015em;border-bottom:1px solid var(--border);padding-bottom:14px}
.path-step{color:var(--text)}
.page h2{font-family:var(--font-display);font-size:1.45rem;line-height:1.5;font-weight:600;margin-top:36px}
.page h3{font-size:1.08rem;line-height:1.55;margin-top:28px}
.page p{margin:12px 0}
.page table{font-size:13.5px;border:1px solid var(--border);border-radius:8px;overflow:hidden}
.page th,.page td{border:1px solid var(--border);padding:8px 11px}
.page th{background:var(--code-bg);font-weight:600;color:var(--text)}
.page code{background:var(--code-bg);border:1px solid var(--border);border-radius:4px;font-family:var(--font-mono);font-size:.9em;padding:1px 5px}
.page pre{background:var(--code-bg);border:1px solid var(--border);border-radius:10px;padding:14px;font-family:var(--font-mono);font-size:13px}
.page blockquote{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 8px 8px 0;padding:8px 14px}
.source-badge{font-size:11.5px;background:var(--code-bg);border:1px solid var(--border);border-radius:6px;padding:4px 10px;color:var(--muted)}
.prereq-bar{border-left:3px solid var(--accent);background:var(--accent-soft);padding:6px 12px;border-radius:0 8px 8px 0}
.misconception-card{background:var(--code-bg);border-left:3px solid var(--bad);border-radius:0 8px 8px 0}
.depth-fragment{background:var(--depth-bg);border:1px solid var(--depth-border);border-radius:10px}
.depth-fragment>summary{color:var(--text)}
.mermaid{background:var(--code-bg);border:1px solid var(--border);border-radius:8px}
@media (max-width:760px){
  .sidebar{width:100%;height:auto;position:static;padding:14px 16px;border-right:0;border-bottom:1px solid var(--border)}
  .sidebar h1{font-size:1.05rem}
  .main{padding:24px 18px 64px;max-width:none}
  .topbar{padding-bottom:10px;margin-bottom:18px}
  .page h1{font-size:1.5rem}
  .page h2{font-size:1.25rem}
  .nav-item{padding:9px 10px;min-height:36px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
@media print{.sidebar,.topbar{display:none!important}.main{max-width:none;padding:0}}
</style>
'''

files = []
for d in sorted(ROOT.iterdir()):
    if not d.is_dir() or not re.match(r'0', d.name):
        continue
    for f in d.glob('*学习伴侣.html'):
        files.append(f)

if not files:
    raise SystemExit('未找到单书学习伴侣')

for f in files:
    s = f.read_text(encoding='utf-8')
    if 'id="visual-skin"' in s:
        print(f'跳过（已套用）{f.relative_to(ROOT)}')
        continue
    # 默认深色
    if '<body>' in s:
        s = s.replace('<body>', '<body data-theme="dark">', 1)
    elif 'data-theme="dark"' not in s[:12000]:
        raise SystemExit(f'{f.name} 未找到 body')
    # 替换浅色与深色 token
    s, n1 = re.subn(r':root\{\s*--bg:#f7f7f8;.*?--depth-border:#ca8a04;\s*\}', LIGHT, s, count=1, flags=re.S)
    s, n2 = re.subn(r'\[data-theme="dark"\]\{\s*--bg:#111318;.*?--depth-border:#a16207;\s*\}', DARK, s, count=1, flags=re.S)
    if n1 != 1 or n2 != 1:
        print(f'警告：{f.name} token 替换 root={n1} dark={n2}')
    # 去掉界面 emoji；先修主题按钮逻辑，再做全局替换
    s = s.replace("themeBtn.textContent = d? '🌙 深色' : '☀️ 浅色';", "themeBtn.textContent = d ? '深色' : '浅色';")
    s = s.replace("themeBtn.textContent = d ? '浅色' : '浅色';", "themeBtn.textContent = d ? '深色' : '浅色';")
    s = s.replace('⬇ 导出进度', '导出进度').replace('⬆ 导入进度', '导入进度')
    s = s.replace('🌙 深色', '浅色').replace('☀️ 浅色', '浅色')
    for a, b in [('📖 出处：','出处：'),('🕸 知识图谱','知识图谱'),('🩺 诊断测试','诊断测试'),('🔬 ',''),('📚 ',''),('🔍 可能的根因','可能的根因'),('🎉 这组题全对','这组题全对'),('本组卡片已全部复习完 🎉','本组卡片已全部复习完')]:
        s = s.replace(a, b)
    # 插入皮肤
    s = s.replace('</head>', SKIN + '</head>', 1)
    f.write_text(s, encoding='utf-8')
    print(f'✓ {f.relative_to(ROOT)}')

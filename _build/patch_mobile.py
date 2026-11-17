#!/usr/bin/env python3
"""移动端：收窄头部，窄表换行，宽表横向滚动，避免数字与英文被逐字拆开。"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
s = s.replace("/*/*/* mobile-table-wrap */", "/* mobile-table-wrap */")
s = s.replace("/*/* mobile-table-wrap */", "/* mobile-table-wrap */")

css = """/* mobile-table-wrap */
@media(max-width:820px){
  .tabs{display:none}
  header{padding:10px 12px}
  .brand{display:block;margin:0 0 6px 0;font-size:16px}
  .hdr-right{float:none;display:flex;flex-wrap:wrap;gap:6px;margin:0}
  #q{flex:1 1 100%;width:100%;font-size:16px}
  #progress-export,#progress-import,#theme-btn{font-size:12px;padding:5px 9px}
  .page table{display:table!important;width:100%!important;max-width:100%!important;table-layout:auto!important;font-size:12px!important}
  .page th,.page td{white-space:normal!important;word-break:break-word!important;padding:6px!important;vertical-align:top}
  .page th:first-child,.page td:first-child{min-width:26px!important;white-space:nowrap!important;text-align:center!important}
  .table-scroll{overflow-x:auto;max-width:100%;margin:10px 0;border:1px solid var(--border);border-radius:8px}
  .table-scroll table{width:1000px!important;min-width:1000px!important;max-width:none!important;table-layout:auto!important}
  .table-scroll th,.table-scroll td{white-space:normal!important;word-break:normal!important;overflow-wrap:anywhere}
  .table-scroll th:first-child,.table-scroll td:first-child{white-space:nowrap!important;width:3em!important;min-width:3em!important}
  .scroll-hint{display:block;font-size:12px;color:var(--muted);margin:0 0 4px;text-align:right}
  .page pre{overflow-x:auto;max-width:100%}
  .page .katex-block{overflow-x:auto}
}"""

js = """function wrapWideTables(){
  document.querySelectorAll('#view table').forEach(t=>{
    if(t.closest('.table-scroll')) return;
    const cols=t.rows.length?t.rows[0].cells.length:0;
    const wide=cols>=5;
    const parent=t.parentElement;
    if(wide || (parent && t.scrollWidth>parent.clientWidth+2)){
      const hint=document.createElement('p');
      hint.className='scroll-hint';
      hint.textContent='表格较宽，可左右滑动 →';
      parent.insertBefore(hint,t);
      const w=document.createElement('div');
      w.className='table-scroll';
      w.dataset.wide=wide?'1':'0';
      parent.insertBefore(w,t);
      w.appendChild(t);
    }
  });
}"""

# Replace any previous mobile block; keep one canonical block.
s = re.sub(r"/* mobile-table-wrap \*/\n@media\(max-width:820px\)\{.*?\n\}\n\n@media print\{",
           css + "\n\n@media print{", s, count=1, flags=re.S)
if "/* mobile-table-wrap */" not in s:
    marker = "@media print{"
    if marker not in s:
        raise SystemExit("未找到 CSS 插入点")
    s = s.replace(marker, css + "\n\n" + marker, 1)

# Replace old wrapper function with the current one.
if "function wrapWideTables" in s:
    s = re.sub(r"function wrapWideTables\(\)\{.*?\n\}\n", js + "\n", s, count=1, flags=re.S)
else:
    marker = "/* ---------- 渲染 ---------- */"
    if marker not in s:
        raise SystemExit("未找到渲染函数插入点")
    s = s.replace(marker, js + "\n" + marker, 1)

# Ensure calls exist exactly once in renderCross/renderBook tails.
s = s.replace("  renderMath();\n  wrapWideTables();", "  renderMath();")
s = s.replace("  renderMath();", "  renderMath();\n  wrapWideTables();")

p.write_text(s, encoding="utf-8")
print("✓ 移动端表格与头部补丁已刷新")

#!/usr/bin/env python3
"""移动端头部收窄：隐藏七行书籍 tab，搜索独占一行，按钮换行。"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'index.html'
s=p.read_text(encoding='utf-8')
css="""
@media(max-width:820px){
  .tabs{display:none}
  header{padding:10px 12px}
  .brand{display:block;margin:0 0 6px 0;font-size:16px}
  .hdr-right{float:none;display:flex;flex-wrap:wrap;gap:6px;margin:0}
  #q{flex:1 1 100%;width:100%;font-size:16px}
  #progress-export,#progress-import,#theme-btn{font-size:12px;padding:5px 9px}
  .page table{display:block;overflow-x:auto;white-space:nowrap;max-width:100%}
  .page th,.page td{white-space:nowrap}
}
"""
marker="@media print{"
if css.strip() not in s:
    s=s.replace(marker,css+"\n"+marker,1)
    p.write_text(s,encoding='utf-8')
    print('✓ 移动端头部已收窄')
else:
    print('- 已存在')

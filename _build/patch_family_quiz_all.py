#!/usr/bin/env python3
"""build_companion.py 的“综合测验”只收 chapterId=__all__ 的题，09 的 36 题分散在各章，
这里把 __quiz_all__ 页改成全书题目聚合，避免独立伴侣显示“无综合题”。"""
import json, re, html, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
f=ROOT/'09-deepseek-family/deepseek-family学习伴侣.html'
s=f.read_text(encoding='utf-8')
m=re.search(r'const DATA = (\{.*?\});\n',s,re.S)
assert m, 'DATA not found'
d=json.loads(m.group(1))
qs=d['manifest'].get('quizzes',[])
def qhtml(q,idx):
    qtype=q.get('type','single'); qid=q.get('id',f'q{idx}')
    parts=[f"<div class='quiz-item' data-qid='{html.escape(qid)}' data-type='{html.escape(qtype)}' data-concept='{html.escape(q.get('relatedConceptId',''))}' data-chapter='{html.escape(q.get('chapterId',''))}'>",
           f"<p class='quiz-q'><b>Q{idx}.</b> {html.escape(q.get('question',''))}</p>"]
    if qtype in ('single','multi'):
        it='radio' if qtype=='single' else 'checkbox'
        parts.append("<div class='quiz-opts'>")
        for oi,o in enumerate(q.get('options') or []):
            parts.append(f"<label class='quiz-opt'><input type='{it}' name='{html.escape(qid)}' value='{oi}'> {html.escape(str(o))}</label>")
        parts.append("</div>")
    parts.append("<div class='quiz-actions'><button class='quiz-check'>检查答案</button><span class='quiz-feedback'></span></div></div>")
    return ''.join(parts)
page='<h1>综合测验（全书 36 题）</h1>'+''.join(qhtml(q,i) for i,q in enumerate(qs,1))+"<p class='quiz-summary'>完成作答后点击「检查答案」查看得分与解析。</p>"
mode=sys.argv[1] if len(sys.argv)>1 else 'full'
if mode=='empty':
    d['rendered']['__quiz_all__']='<p>（无综合题）</p>'
else:
    d['pages']['__quiz_all__']['html']=page
    d['rendered']['__quiz_all__']=page
new=json.dumps(d,ensure_ascii=False,separators=(',',':'))
s=s[:m.start(1)]+new+s[m.end(1):]
f.write_text(s,encoding='utf-8')
print('patched quiz/all:',len(qs),'questions')

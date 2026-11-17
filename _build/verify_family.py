#!/usr/bin/env python3
"""逐页检查 09 分册：14 章、13 概念、每章测验页、移动端无溢出。"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
man=json.load(open(ROOT/'09-deepseek-family/manifest.json',encoding='utf-8'))
res=[]
def ck(n,ok,extra=''):
 res.append({'check':n,'pass':bool(ok),'extra':extra}); print(('PASS ' if ok else 'FAIL ')+n+(' | '+extra if extra else ''))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/local/bin/chromium',args=['--no-sandbox'])
 pg=b.new_page(viewport={'width':1440,'height':900})
 errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
 pg.goto('file://'+str(ROOT/'index.html')); pg.wait_for_timeout(500)
 # all chapters
 for ch in man['chapters']:
  pg.evaluate(f"location.hash='#/book/deepseek-family/chapter/{ch['id']}'"); pg.wait_for_timeout(450)
  txt=pg.inner_text('#view')
  ck('书内章 '+ch['id'], '页面不存在' not in txt and len(txt)>800, f'{len(txt)} 字')
  ck('书内章公式/图 '+ch['id'], pg.eval_on_selector_all('.katex','e=>e.length')+pg.eval_on_selector_all('.mermaid svg','e=>e.length')>0, f"{pg.eval_on_selector_all('.katex','e=>e.length')} katex / {pg.eval_on_selector_all('.mermaid svg','e=>e.length')} svg")
 # all concepts
 for c in man['concepts']:
  pg.evaluate(f"location.hash='#/book/deepseek-family/concept/{c['id']}'"); pg.wait_for_timeout(400)
  txt=pg.inner_text('#view')
  ck('概念 '+c['id'], '页面不存在' not in txt and len(txt)>300, f'{len(txt)} 字')
 # per-chapter quizzes
 for ch in man['chapters']:
  n=sum(1 for q in man['quizzes'] if q['chapterId']==ch['id'])
  pg.evaluate(f"location.hash='#/book/deepseek-family/quiz/{ch['id']}'"); pg.wait_for_timeout(400)
  got=pg.eval_on_selector_all('.quiz-item','e=>e.length')
  ck('测验页 '+ch['id'], got==n, f'{got}/{n}')
 # mobile all chapters
 pg.set_viewport_size({'width':390,'height':844})
 for ch in man['chapters']:
  pg.evaluate(f"location.hash='#/book/deepseek-family/chapter/{ch['id']}'"); pg.wait_for_timeout(400)
  sw=pg.evaluate('document.documentElement.scrollWidth')
  ck('移动端宽 '+ch['id'], sw<=390, str(sw))
 # standalone
 p2=b.new_page(viewport={'width':1440,'height':900})
 p2.goto('file://'+str(ROOT/'09-deepseek-family/deepseek-family学习伴侣.html')); p2.wait_for_timeout(700)
 for ch in man['chapters']:
  p2.evaluate(f"location.hash='#/chapter/{ch['id']}'"); p2.wait_for_timeout(400)
  txt=p2.inner_text('#view')
  ck('独立章 '+ch['id'], '页面不存在' not in txt and len(txt)>800, f'{len(txt)} 字')
 for c in man['concepts']:
  p2.evaluate(f"location.hash='#/concept/{c['id']}'"); p2.wait_for_timeout(350)
  txt=p2.inner_text('#view')
  ck('独立概念 '+c['id'], '页面不存在' not in txt and len(txt)>300, f'{len(txt)} 字')
 p2.evaluate("location.hash='#/quiz/all'"); p2.wait_for_timeout(500)
 ck('独立综合测验', p2.eval_on_selector_all('.quiz-item','e=>e.length')==42, str(p2.eval_on_selector_all('.quiz-item','e=>e.length')))
 ck('控制台', len(errs)==0, ' || '.join(errs[:2]))
 b.close()
ok=sum(1 for r in res if r['pass']); print(f'\n=== {ok}/{len(res)} 通过 ===')
json.dump(res,open(ROOT/'_build/verify_family.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
sys.exit(0 if ok==len(res) else 1)

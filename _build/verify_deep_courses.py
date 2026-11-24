#!/usr/bin/env python3
"""验证六套深潜课：目录、公式、测验、移动端与页间跳转。"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
COURSES=[
('07-transformer-deep',15,False),('08-svm-deep',16,False),
('10-backprop-deep',10,True),('11-moe-mla-deep',10,True),('12-probability-eval-deep',10,True),('13-train-infer-deep',9,True),
('14-math-deep',12,True),('15-python-deep',10,True),('16-classical-ml-deep',12,True),('17-cnn-rnn-deep',10,True),
('18-rl-grpo-deep',10,True),('19-deepseek-arch-deep',13,True),('20-multimodal-deep',9,True),('21-eval-safety-deep',9,True),('22-serving-deep',9,True)]
res=[]
def ck(n,ok,extra=''):
 res.append({'check':n,'pass':bool(ok),'extra':extra}); print(('PASS ' if ok else 'FAIL ')+n+(' | '+extra if extra else ''))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/local/bin/chromium',args=['--no-sandbox'])
 for slug,secs,new in COURSES:
  pg=b.new_page(viewport={'width':1440,'height':900})
  errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('file://'+str(ROOT/slug/'index.html'),timeout=60000); pg.wait_for_timeout(4000)
  ck(f'{slug} 打开', ('深潜课' in pg.title()) if new else ('交互式学习' in pg.title()), pg.title())
  ck(f'{slug} 节数', pg.eval_on_selector_all('section','e=>e.length')==secs, str(pg.eval_on_selector_all('section','e=>e.length')))
  ck(f'{slug} 目录', pg.eval_on_selector_all('.nav-item','e=>e.length')==secs, str(pg.eval_on_selector_all('.nav-item','e=>e.length')))
  ck(f'{slug} 公式', pg.eval_on_selector_all('.katex','e=>e.length')>1, str(pg.eval_on_selector_all('.katex','e=>e.length')))
  if new:
    q=pg.eval_on_selector_all('.quiz','e=>e.length')
    ck(f'{slug} 测验', q==5, str(q))
    ans=pg.eval_on_selector('.quiz','e=>+e.dataset.answer')
    pg.eval_on_selector_all('.quiz .opt', f'(els)=>els[{ans}].click()')
    pg.wait_for_timeout(200)
    fb=pg.inner_text('.quiz .fb')
    ck(f'{slug} 正确反馈', '正确' in fb, fb[:40])
    wrong=1 if ans==0 else 0
    pg.eval_on_selector_all('.quiz .opt', f'(els)=>els[{wrong}].click()')
    pg.wait_for_timeout(200)
    ck(f'{slug} 错误反馈', '不对' in pg.inner_text('.quiz .fb'))
  # 切到下一节
  if new:
    pg.click('#next'); pg.wait_for_timeout(500)
    vis=pg.eval_on_selector_all('section','els=>els.filter(e=>e.style.display!=="none").length')
    ck(f'{slug} 下一节', vis==1, str(vis))
  else:
    pg.eval_on_selector_all('.nav-item','els=>els[1].click()'); pg.wait_for_timeout(400)
    ck(f'{slug} 目录切换', pg.eval_on_selector_all('.nav-item.active','e=>e.length')==1)
  # 移动端
  pg.set_viewport_size({'width':390,'height':844}); pg.wait_for_timeout(300)
  ck(f'{slug} 移动端', pg.evaluate('document.documentElement.scrollWidth')<=390, str(pg.evaluate('document.documentElement.scrollWidth')))
  ck(f'{slug} 控制台', len(errs)==0, ' || '.join(errs[:2]))
  pg.close()
 b.close()
ok=sum(1 for r in res if r['pass']); print(f'\n=== {ok}/{len(res)} 通过 ===')
json.dump(res,open(ROOT/'_build/verify_deep_courses.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
sys.exit(0 if ok==len(res) else 1)

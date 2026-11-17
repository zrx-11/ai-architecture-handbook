#!/usr/bin/env python3
"""修正总入口里深潜课的相对链接。

总入口是单文件 SPA，文档基址是仓库根目录；从 #/... 路由点击 `../07-...`
会解析到域名根目录，部署后 404。这里只改构建产物 index.html，
不改各分册源 Markdown（分册伴侣从自己的目录打开时 `../` 才是对的）。
"""
from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
for slug in ('01-foundations', '02-paper-teardown', '03-architecture', '04-machine-learning', '05-neural-networks', '06-deep-learning', '09-deepseek-family', '07-transformer-deep', '08-svm-deep', '10-backprop-deep', '11-moe-mla-deep', '12-probability-eval-deep', '13-train-infer-deep', '14-math-deep', '15-python-deep', '16-classical-ml-deep', '17-cnn-rnn-deep', '18-rl-grpo-deep', '19-deepseek-arch-deep', '20-multimodal-deep', '21-eval-safety-deep', '22-serving-deep'):
    s = s.replace(f'../{slug}/', f'{slug}/')
    s = s.replace(f'../{slug}', f'{slug}')
p.write_text(s, encoding='utf-8')
print('patched deep-course links in index.html')

#!/usr/bin/env python3
"""修正总入口里深潜课的相对链接。

总入口是单文件 SPA，文档基址是仓库根目录；从 #/... 路由点击 `../07-...`
会解析到域名根目录，部署后 404。这里只改构建产物 index.html，
不改各分册源 Markdown（分册伴侣从自己的目录打开时 `../` 才是对的）。
"""
from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
for slug in ('07-transformer-deep', '08-svm-deep'):
    s = s.replace(f'../{slug}/', f'{slug}/')
    s = s.replace(f'../{slug}', f'{slug}')
p.write_text(s, encoding='utf-8')
print('patched deep-course links in index.html')

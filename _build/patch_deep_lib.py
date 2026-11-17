#!/usr/bin/env python3
"""把首页资料库的两套深潜课扩成六套。"""
from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
OLD="""      + `<a class="lib-item" href="${encodeURI('07-transformer-deep/index.html')}" target="_blank"><b>Transformer 深潜</b><span>15 节 · 179 个推导步骤</span></a>`
      + `<a class="lib-item" href="${encodeURI('08-svm-deep/index.html')}" target="_blank"><b>SVM 深潜</b><span>16 节 · 1355 个公式</span></a>`"""
NEW="""      + `<a class="lib-item" href="${encodeURI('07-transformer-deep/index.html')}" target="_blank"><b>Transformer 深潜</b><span>15 节 · 179 个推导步骤</span></a>`
      + `<a class="lib-item" href="${encodeURI('08-svm-deep/index.html')}" target="_blank"><b>SVM 深潜</b><span>16 节 · 1355 个公式</span></a>`
      + `<a class="lib-item" href="${encodeURI('10-backprop-deep/index.html')}" target="_blank"><b>反向传播与优化器</b><span>10 节 · 手算梯度到 Adam</span></a>`
      + `<a class="lib-item" href="${encodeURI('11-moe-mla-deep/index.html')}" target="_blank"><b>MoE 与 MLA</b><span>10 节 · 路由与 KV 账</span></a>`
      + `<a class="lib-item" href="${encodeURI('12-probability-eval-deep/index.html')}" target="_blank"><b>概率、损失与评估</b><span>10 节 · 交叉熵 / PR / AUC</span></a>`
      + `<a class="lib-item" href="${encodeURI('13-train-infer-deep/index.html')}" target="_blank"><b>训练与推理账本</b><span>9 节 · FLOPs / KV / 并行</span></a>`"""
if OLD not in s:
 print('OLD block not found'); raise SystemExit(1)
s=s.replace(OLD,NEW,1); p.write_text(s,encoding='utf-8'); print('patched 6 deep courses')

# 模式与框架库

## 框架 1：六问读卡法

拿到任何一张模型卡，按顺序问：

1. `architectures` / `model_type` 是什么？
2. 总参数、激活参数各多少？
3. 注意力是 MHA/GQA/MLA/DSA/CSA/HCA/CSA2 中的哪一种？
4. FFN 是 dense 还是 MoE？多少路由专家、多少共享专家、top-k 多少？
5. 上下文多长、训练 token 多少、精度是什么？
6. 许可证是什么？

这六个问题能把“新架构”和“同架构新 checkpoint”分开。

## 框架 2：代际主线

| 代 | 解决的问题 | 关键结构 |
|---|---|---|
| Dense | 先把语言模型跑起来 | LLaMA 式 decoder、GQA |
| MoE | 同样算力下扩大容量 | 细粒度专家、共享专家、top-k |
| V2 | KV cache 太大 | MLA、160 路由 |
| V3 | 规模与训练稳定性 | 256 路由、MTP、无辅助损失均衡、FP8 |
| V3.2 | 长上下文与 Agent | DSA、Agent RL |
| V4 | 1M 上下文成本 | token 压缩 + DSA、mHC、Muon |
| V4.1 | KV cache 再压 | CED、CSA2、Engram、DSpark、FP4 KV |

## 框架 3：选型顺序

任务 → 显存 → 延迟 → 上下文 → 许可证。

不要反过来从“哪个模型最大”开始。V4-Pro 1.6T 对单机没有意义；V2-Lite 16B/2.4B 才是学习实验的入口。

## 决策规则

- 本地实验、显存 < 24 GB：V2-Lite、OCR、Janus-Pro-1B。
- 通用对话/代码、有 8 卡 A100/H100：V3.1 671B/37B。
- 1M 文档 Agent、要低成本：V4.1-Flash 或 V4-Flash。
- 最高质量、不计成本：V4-Pro。
- Lean 形式化：Prover-V2-671B；自然语言数学证明：Math-V2。
- 文档 OCR：OCR2；视觉理解：VL2；理解+生成：Janus-Pro。
- 商用且不想读自定义条款：优先 MIT/Apache 2.0 的 checkpoint。

## 反模式

- **只看总参数**：MoE 的算力看激活参数，显存看总参数，两个数要分开。
- **把 HF 权重总量当主模型**：V3 的 685B 含 14B MTP；V4.1 的 763B 含 196B Engram。
- **把同家族 checkpoint 当新架构**：V3-0324、V3.1、V3.1-Terminus 结构相同。
- **把“开放权重”写成“OSI 开源”**：DeepSeek Model License 不是 MIT/Apache。
- **用 V4-Pro 的分数套 V4-Flash**：两者不是同一档。
- **忽略压缩的代价**：CSA/HCA 会丢细节，CED 的解码器表达受编码器末端限制。

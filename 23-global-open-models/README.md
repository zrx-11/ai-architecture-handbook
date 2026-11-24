# 全球开源模型全谱

这是“AI 架构学习手册”的第八本分册，也是主线第 6 步的全球对照册：把 DeepSeek 案例里练出的读法，扩到全世界官方公开、权重可下载的主流开放模型。

## 规模

- 16 章：边界、世界地图、Llama、Qwen、Mistral、Gemma、Phi、北美其他、中国其他、非 Transformer、MoE、多模态、注意力与长上下文、许可证与评测、config、101 行索引。
- 12 个概念页、53 道测验、48 张抽认卡、70 条术语、6 个判断模式、1 张速查表、1 条 7 步学习路径。
- 单文件入口：`global-open-models学习伴侣.html`（构建后由 `apply_visual_theme.py` 注入深色视觉）。

## 收录口径

只收**官方公开发布、权重可下载、有明确架构说明**的主要家族；同一家族的量化、微调、合并版本在附录索引里作为同族代表出现，不逐条拆 config。表里的“10M/1M/262K”是模型卡或 config 标称，不等于实测可用长度。

## 七步路径

1. 边界与地图（第 1–2 章）：开放权重/开源/许可证；六种骨架。
2. Llama 与 Qwen（第 3–4 章）：decoder-only 基线；dense/MoE/线性混合全尺寸树。
3. Mistral、Gemma、Phi（第 5–7 章）：滑窗、局部/全局、小模型数据路线。
4. 北美与中国其他（第 8–9 章）：Falcon/BLOOM/OLMo/DBRX；GLM/Kimi/MiniMax/InternLM。
5. 非 Transformer 与 MoE（第 10–11 章）：RWKV/Mamba/Jamba/Griffin/xLSTM；总参/激活/路由。
6. 多模态与注意力（第 12–13 章）：ViT patch、连接器、早期/晚期融合；MHA/GQA/MLA/滑窗/稀疏/线性。
7. 许可证、评测与 config（第 14–16 章）：许可证矩阵、污染、选型、字段读法、101 行索引。

## 数据与出处

- `data/global-model-index.json`：101 行结构化家族索引，字段为 `family, model, params, context, architecture, license, region`。
- 事实来源以 HuggingFace 模型卡与 `config.json` 为主：`https://huggingface.co/<model>/raw/main/config.json`、`https://huggingface.co/api/models?author=<org>`。
- 少数 gated 模型直接读官方 config 会 401，使用公开镜像 config 或模型卡；正文对无法确认的字段标“未公开/待确认”，不编造。

## 构建

```bash
python3 ../<zhishu>/scripts/build_companion.py --manifest manifest.json --out global-open-models学习伴侣.html
python3 ../<zhishu>/scripts/apply_visual_theme.py --file global-open-models学习伴侣.html
```

`manifest.json` 是唯一数据源；改章节、测验、卡片、术语后重新构建，不要手改 HTML。

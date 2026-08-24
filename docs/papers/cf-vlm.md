---
title: "CF-VLM: Counterfactual Vision-Language Fine-tuning"
description: 以文本和图像双侧最小反事实及三项因果对齐损失提升 VLM 组合与反事实判别能力
authors: [Jusheng Zhang, Kaitong Cai, Yijia Fan, Jian Wang, Keze Wang]
venue: NeurIPS
year: 2025
resource_type: 方法论文
direction: Training / Alignment
hallucination_type: [Compositional hallucination, Object hallucination, Attribute hallucination, Relation hallucination]
method_level: [Data-level, Representation-level]
training: Full fine-tuning
status: 已精读
source_status: NeurIPS 2025 官方论文已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://proceedings.neurips.cc/paper_files/paper/2025/hash/541b6d155146d142a5e10d787d1d430f-Abstract-Conference.html
overview_figure: ../assets/images/papers/cf-vlm-overview.png
overview_figure_source: Figure 2 from the official NeurIPS 2025 paper
tags: [CF-VLM, Counterfactual, Compositional reasoning, SDXL, NeurIPS]
---

# CF-VLM

<div class="paper-meta"><span>NeurIPS 2025</span><span>Training / Alignment</span><span>Counterfactual fine-tuning</span><span>已精读</span></div>

[论文原文](https://proceedings.neurips.cc/paper_files/paper/2025/hash/541b6d155146d142a5e10d787d1d430f-Abstract-Conference.html){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>CF-VLM 围绕事实图文对同时生成文本侧和图像侧最小反事实，并以基础跨模态对齐、场景级反事实区分和细粒度因果区分三项损失，迫使模型响应对象、属性、关系的局部改变。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/cf-vlm-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/cf-vlm-overview.png" alt="CF-VLM 官方方法总览"></a><figcaption>官方方法概览图（论文 Figure 2）：事实锚点、双侧反事实生成与三项训练目标。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 目标 | 让 VLM 对对象、属性、关系的最小因果改变敏感，而非只学全局共现 |
| 文本反事实 | Qwen2-72B-Instruct 以 3-shot CoT 改写描述 |
| 图像反事实 | SDXL Base + Refiner 生成与改写文本一致的图像 |
| 损失 | foundational alignment、scenario discrimination、fine-grained causal discrimination |
| 评测 | ConMe、ARO、VL-Checklist；另查 ImageNet 和跨模态检索保持 |

## 2. 研究背景

视觉语言预训练依赖网络图文共现，容易把“人—骑—马”等高频结构当作整体模板，对局部对象、属性或关系替换不敏感。CF-VLM 认为仅加随机 negative 太容易，只有最小反事实才能迫使模型识别哪一因素改变了图文一致性。

它更接近组合推理/匹配而不是开放生成幻觉缓解；因此应作为反事实表示学习证据，而不能直接当作 CHAIR 改善结论。合成图像的真实性、编辑目标是否唯一变化以及生成器偏差，是构念效度核心。

## 3. 方法详解

从 factual image-text pair 出发，文本生成器分别替换 object、attribute 或 relation；图像生成器据此合成对应 counterfactual image。最终得到事实锚点、文本反事实、图像反事实及匹配的双反事实组合。

基础对齐 loss 保留正常图文匹配；场景级区分要求事实与不匹配反事实拉开；细粒度因果 loss 约束模型对最小变量改变敏感。论文在 CLIP ViT-B/32、Qwen-VL 和 LLaVA 等架构上验证，训练批次事实与反事实约 1:1。主实验报告三 seed 平均，这是其统计设计的优点。

## 4. 实验设计

### 4.1 设置

CLIP 路线使用 CC12M/CC3M，LLM-based 路线微调 Qwen-VL 与 LLaVA。核心 benchmark 为 ConMe 的 Replace-Obj/Attr/Rel、ARO 的 VG-Rel/VG-Attr 与 VL-Checklist；一般能力检查 ImageNet zero-shot 和 COCO/Flickr retrieval。对照包含标准 FT、text-negative FT 及结构化 CLIP 方法。

### 4.2 主结果

| 模型 / 指标 | 对照 | CF-VLM | 解读 | 来源 |
|---|---:|---:|---|---|
| ViT-B/32 ConMe Avg ↑ | Std FT 54.43 | 59.13 | +4.70 pt | Table 1 |
| ViT-B/32 ARO Avg ↑ | Std FT 71.2 | 89.35 | 大幅提升组合判别 | Table 1 |
| ViT-B/32 VL-Checklist Avg ↑ | Std FT 74.6 | 88.4 | 对对象/属性/关系均改善 | Table 1 |
| Qwen-VL 7B ConMe Avg ↑ | Std FT 82.6；TextNeg 84.13 | 87.57 | 双侧反事实优于文本负例 | Table 2 |
| Qwen-VL 7B ARO Avg ↑ | TextNeg 87.5 | 93.2 | 关系/属性共同提升 | Table 2 |
| LLaVA ConMe Avg ↑ | Std FT 61.77 | 65.3 | 跨架构迁移 | Table 2 |

主结果证明反事实训练提高 compositional discrimination。一般能力图中多项 retrieval 有保持或改善，但 ImageNet 绝对值较低，且这些指标不是自由生成 hallucination；使用时应明确外推边界。

### 4.3 消融与分析实验

Table 3 中只用随机负例的 ConMe/ARO 为 54.4/71.2，text-only 55.9/78.65，image-only 56.1/78.25，双侧 CF-VLM 达 59.1/89.35；说明图文两侧反事实具有互补信息。Table 4 对三项 loss 做全组合消融：完整模型 ConMe Avg 59.1，任意去掉一项降至 57.3–58.0，仅单项约 55.4–56.2。结果支持完整目标，但缺“同生成器、非因果属性等量变化”的 matched sham；生成图可能通过风格或质量被识别。

## 5. 亮点与贡献

- 同时生成图像侧和文本侧反事实，避免只学语言替换。
- 对象、属性、关系三类最小改变有明确任务拆分。
- 多架构、三 seed 和完整 loss 组合消融提升可信度。

## 6. 局限

SDXL 合成可能改变非目标区域；LLM 改写可能引入语法/长度信号。训练成本高，CC12M 级数据与 200K steps 难低成本复现。核心指标偏检索/判别，未直接证明自由生成减少对象虚构。合成域到自然图的 transport 仍需专门实验。

## 7. 与我的研究关系

CF-VLM 是检验“成对反事实训练是否带来真正视觉敏感性”的关键参考。最值得借鉴的是双侧因果结构和 loss 分解；最需要补足的是目标保持、matched sham 与自由生成效用，而不是直接复制大规模生成流水线。

## 8. 可执行的后续实验

1. 为每个编辑构造同编辑器 matched sham，测目标与非目标变化。
2. 用真实图片中的自然最小对验证合成训练迁移。
3. 将训练后模型放到 CHAIR/THRONE，联合报告 Recall 与长度。
4. 比较 text-only、image-only、双侧反事实在等样本/等算力下的收益。

## 9. 复现清单

- [x] 官方 Figure 2、主表、双侧数据与 loss 消融已登记
- [ ] 固定 Qwen/SDXL 版本、prompt、seed 和过滤器
- [ ] 保存编辑前后图像、mask 与非目标差异分数
- [ ] 报告三 seed 均值/标准差和训练成本
- [ ] 增加自由生成 hallucination 终点

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 图文双侧反事实训练完整 |
| 证据强度 | 4/5 | 多架构、多 seed 与组件消融 |
| 构念效度 | 3/5 | 合成编辑仍可能有伪迹 |
| 相关性 | 5/5 | 直接对应反事实视觉学习 |

## 11. 来源边界

本文依据 NeurIPS 2025 官方论文整理。数字来自 Tables 1–4；对自由生成、matched sham 和自然域 transport 的讨论属于本站分析。

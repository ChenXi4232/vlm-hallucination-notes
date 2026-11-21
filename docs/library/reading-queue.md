---
title: 待读与待整理来源
tags:
  - Reading queue
---

# 待读与待整理来源

这里只保留尚未形成 Deep Paper Note 的来源。PDF 文件不直接提交到公开仓库，避免体积、版权和版本混乱。

| 来源 | 计划类型 | 目标方向 | 状态 |
|---|---|---|---|
| [HaloProbe: Bayesian Detection and Mitigation of Object Hallucinations in Vision-Language Models](https://proceedings.mlr.press/v306/zohrabi26a.html)（ICML 2026） | 高优先级机制/检测论文 | Attention Head / Evaluation | P1：PMLR正文、OpenReview入口与官方代码齐；优先核对token位置/对象重复混淆、Simpson's paradox与Bayesian reranking成本 |
| [OmniHallu: Unified Hallucination Detection for Cross-Modal Comprehension and Generation in Multimodal Large Language Models](https://aclanthology.org/2026.findings-emnlp.644/)（arXiv:2609.11244；EMNLP 2026 Findings） | 高优先级 benchmark | Evaluation / Long-form | 正式 Anthology 论文页已核对；跨模态 claim 标注、许可和 evaluator 协议待精读 |
| VidHalLoc: Temporal Localization of Hallucinations in Long-form Video-Language Generation (arXiv:2609.09895 v1) | 候选 benchmark / detection | Evaluation / Long-form | 待读：需核对 temporal annotation、长输出长度混淆和公开数据许可 |
| Does Playing it Safe Count as Faithfulness? Reassessing LVLM Hallucination Mitigation Methods (arXiv:2609.01888 v1) | 高优先级评测审计 | Evaluation / Recall Trade-off | 暂停收录：摘要称 4 个 benchmarks，正文主协议称 3 个，公开代码仓库又列 CHAIR/AMBER/MMHal/MMStar；待版本澄清 |
| ReWEIGH the Evidence: Calibrating Token-Level Ordinal Visual Evidence to Mitigate Hallucinations in Large Vision-Language Models (arXiv:2608.19075 v1) | 候选方法论文 | Token / Logit | 待读：与 SADT/PatchGate 的增量和代码状态待核对 |
| Targeting the Attention Heads Behind Object Hallucination in LLaVA (arXiv:2608.24966 v1) | 候选机制/负结果 | Attention Head / Path | 待读：需完整核对 head mining、随机头对照与干预退化证据 |
| LLM Unlearning Should Be Form-Independent | 相邻工作 | Form-independent intervention | 相关性待判断 |

## 已迁移

| 来源 | Deep Paper Note |
|---|---|
| MLLMs Hallucinate when Information Distribution Drifts in Synergy Heads | [HEAL](../papers/heal-synergy-heads.md) |
| Hallucination-aware Intermediate Representation Edit | [HIRE](../papers/hire-intermediate-representation-edit.md) |
| Hallucination Begins Where Saliency Drops | [Saliency / SGRS / LocoRE](../papers/hallucination-begins-where-saliency-drops.md) |
| Mitigating Object Hallucination via Image-Grounded Guidance | [MARINE](../papers/marine-image-grounded-guidance.md) |
| Dynamic Multimodal Activation Steering | [DMAS](../papers/dynamic-multimodal-activation-steering.md) |
| HulluEdit | [HulluEdit](../papers/hulluedit.md) |
| AdaIAT | [AdaIAT](../papers/adaiat.md) |
| Reallocating Attention Across Layers to Reduce Multimodal Hallucination | [Reallocating Attention](../papers/reallocating-attention.md) |
| Thinking in Uncertainty / LEAD | [LEAD](../papers/lead-entropy-aware-decoding.md) |
| VisER: Visual Evidence and Reliance for Object Hallucination Detection in LVLMs | [VisER](../papers/viser.md) |

## 进入论文库的条件

- [ ] 核对 title、authors、venue/year、原文链接与当前版本；
- [ ] 明确与 VLM hallucination 主线的相关性，避免只因术语相似而收录；
- [ ] 若进入方法库，补齐 benchmark、baseline、关键 ablation 与官方方法图；
- [ ] 记录资料缺失和不可核验边界。

## CVPR 2026候选（尚未精读）

评分与取舍见[本轮核验](../reading-notes/research-atlas-20261003.md)。

| 优先级 | 来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [Beyond the Global Scores: Fine-Grained Token Grounding as a Robust Detector of LVLM Hallucinations](https://openaccess.thecvf.com/content/CVPR2026/html/Nguyen_Beyond_the_Global_Scores_Fine-Grained_Token_Grounding_as_a_Robust_CVPR_2026_paper.html)（CVPR2026主会） | 暂停晋升：正文、补充和代码有模型及解码口径差异。见[复现审计](../reading-notes/research-atlas-20261119.md#beyond-the-global-scores) |
| P1 | [CORAL v2](https://arxiv.org/abs/2609.38979v2) | 核对FDR定理假设、视觉扰动对称性、对象依赖及官方录用证据；作者称NeurIPS2026录用 |
| P2 | [GHOST-Q](https://arxiv.org/abs/2609.29999) | 预印本；待完整读取跨精度配对统计与生成预算审计 |

### CVPR 主会历史补齐

- [MIOH](../papers/mioh.md) 已完成正文、补充与版本核验。完整题库、代码和许可仍待核。
- P1：[OSI-Bench](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_From_Indoor_to_Open_World_Revealing_the_Spatial_Reasoning_Gap_CVPR_2026_paper.html)。有[作者项目](https://mingrui-wu.github.io/osi-bench/)，待查盲测、合成异常场景、度量真值与领域偏移。
- P2：[VisRes Bench](https://openaccess.thecvf.com/content/CVPR2026/html/Tortei_VisRes_Bench_On_Evaluating_the_Visual_Reasoning_Capabilities_of_VLMs_CVPR_2026_paper.html)。核对图谜及自然图像的推理设置、文本线索残留和数据许可。

## NeurIPS 2026官方论文页候选（未精读）

官方Downloads已列题名/event页，不等于正式proceedings已经出版。以下仅为候选摘要筛选，尚未通过正文/补充/代码/decision一致性闸门；评分与覆盖见[2026-10-17核验](../reading-notes/research-atlas-20261017.md)。

| 优先级 | 官方来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [Robustness of Internal Signals](https://neurips.cc/virtual/2026/poster/139199)（原 In-Depth Analysis） | token位置基线、跨架构检测、视觉/语言错误分型与image-level split |
| P1 | [VerDA](https://neurips.cc/virtual/2026/poster/149428) | head-wise cues、去冗余和距离衰减独立消融；recall与实际成本 |
| P1 | [Focus Matters](https://neurips.cc/virtual/2026/poster/155092) | [arXiv v2](https://arxiv.org/abs/2604.03556v2)已知；核对 encoder phase、attention-value、同图均值替换与随机对照 |
| P1 | [HALMES](https://neurips.cc/virtual/2026/poster/153080) | [arXiv v1](https://arxiv.org/abs/2611.09957v1)已有公开入口；核对前驱信息、触发率、真对象误伤和同预算对照 |
| P2 | [Correction Space Steering](https://neurips.cc/virtual/2026/poster/150994) | 空间学习与坐标预测成本、秩假设和类型外推 |
| P2 | [VGDPO](https://neurips.cc/virtual/2026/poster/154431) | squeezing定义、视觉重权、监督与chosen/rejected概率轨迹 |
| P2 | [PAVE](https://neurips.cc/virtual/2026/poster/150489) | 逐图 prefill 基底与离线激活子空间；比对固定基底、校准划分和等预算 Recall |
| 原P1更新 | [CORAL](https://neurips.cc/virtual/2026/poster/150874) | 官方入口补齐；OpenReview验证未越过；FDR定理、依赖与对称性待核 |

既有 [Dual-Pathway Note](../papers/dual-pathway-circuits.md) 已完成 v1/v2 差异和作者代码静态核验，保留原收录日。

## ICML 2026正式卷候选

PMLR 306于2026-09-29公开。本轮完成全卷标题筛选，并对19篇直接VLM/MLLM幻觉命中读取官方摘要；以下按对现有机制路线的新增价值排序。评分与扫描范围见[2026-10-10核验](../reading-notes/research-atlas-20261010.md)。

| 优先级 | 来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [HaloProbe](https://proceedings.mlr.press/v306/zohrabi26a.html) | 核对位置/重复混淆控制、分层贝叶斯假设、检测与reranking预算；读取公开评审与代码 |
| P1 | [Mitigating Hallucinations via Causal Route Gating](https://proceedings.mlr.press/v306/cheng26d.html) | 核对视觉/文本route定义、梯度门控是否因果、一次前向+反向的实际开销与随机route对照 |
| P1 | [Steer Where It Matters: Token-Level Visual-Sensitivity Steering](https://proceedings.mlr.press/v306/zhang26cg.html) | 核对visual-sensitivity proxy、触发率、跨模型阈值与recall/长度权衡 |
| P1 | [Inter-Layer Visual Attention Discrepancy](https://proceedings.mlr.press/v306/xie26m.html) | 核对层间差异与对象位置混淆、代码实现、早晚层选择和随机层对照 |
| P1 | [Adaptive Residual-Update Steering / RUDDER](https://proceedings.mlr.press/v306/zou26e.html) | 核对prefill方向估计、吞吐口径、逐token触发与跨prompt稳定性 |
| P1 | [Beyond Blind Noising: Disentangled Visual Rectification](https://proceedings.mlr.press/v306/chen26dz.html) | 核对SSL encoder依赖、VCD噪声漂移诊断及同预算对照 |
| P2 | [MM-Snowball](https://proceedings.mlr.press/v306/jiang26t.html) | 核对多轮标注、错误传播定义、turn长度与历史可见性混淆、数据许可 |
| P2 | [DOUBT](https://proceedings.mlr.press/v306/chen26dl.html) | 核对vMF分布假设、对象抽取器依赖、held-out迁移与检测阈值校准 |

## EMNLP 2026 正式卷候选

本轮扫描范围、分级和证据缺口见 [11 月 19 日来源核验](../reading-notes/research-atlas-20261119.md)。

| 优先级 | 正式来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [Where Hallucinations Live](https://aclanthology.org/2026.emnlp-main.2005/) · 主会 | 跨架构 VQ circuit、开放生成分型、同位置组件对照 |
| P1 | [BRACS](https://aclanthology.org/2026.emnlp-main.1662/) · 主会 | grounding barrier、触发率与同强度干预及 Recall 对照 |
| P1 | [Global-to-Local Visual Attention Correction](https://aclanthology.org/2026.emnlp-main.2272/) · 主会 | 尾部幻觉、位置和长度混淆、局部选择与 Recall |
| P2 | [Target-Binding](https://aclanthology.org/2026.emnlp-main.691/) · 主会 | 多图错绑的视觉源标注、图像顺序与距离控制 |
| P1 | [SAFE](https://aclanthology.org/2026.findings-emnlp.140/) · Findings | 同前缀 real/vision-ablated 对照、视觉干预和分布外效应 |
| P2 | [OViP](https://aclanthology.org/2026.findings-emnlp.674/) · Findings | diffusion 负图的单对象操控、训练预算和覆盖保留 |

## ACM MM 2026 正式卷候选

| 优先级 | 来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [Beyond Language Priors](https://doi.org/10.1145/3767308.3836058) | 区分视觉误读、对象缺失和语言先验；对照实际视觉依赖和生成覆盖 |
| P2 | [Beyond the Logits / LAVIG](https://doi.org/10.1145/3767308.3835945) | 层级选择、覆盖与同预算开销，正文和补充待核验 |

## 补充预印本候选

| 优先级 | 来源 | 下一步证据闸门 |
|---|---|---|
| P1 | [Say Less, Hallucinate Less?](https://arxiv.org/abs/2611.23179) | 对照早 EOS、生成长度和对象覆盖；预印本评估代码尚待公开 |
| P2 | [FlashAttention with Statistics](https://arxiv.org/abs/2610.21483) | 相邻 LLM 系统工作；核对 VLM 多模态注意统计、短上下文开销与 kernel 适配 |
| P1 | [Contrast Where It Matters](https://arxiv.org/abs/2611.25524v1) | 预印本。审计动态视觉证据选区、全局对照、分布偏移和 Recall，与已有对比解码工作逐项区分 |

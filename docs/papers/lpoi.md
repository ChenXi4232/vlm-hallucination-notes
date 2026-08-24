---
title: "LPOI: Listwise Preference Optimization for Vision Language Models"
description: 通过对象可见度连续变化构造列表偏好，让 VLM 学习视觉证据强度与对象陈述概率的单调关系
authors: [Fatemeh Pesaran Zadeh, Yoojin Oh, Gunhee Kim]
venue: ACL
year: 2025
resource_type: 方法论文
direction: Training / Alignment
hallucination_type: [Object hallucination]
method_level: [Listwise preference, Training-level]
training: LoRA fine-tuning
status: 已精读
source_status: ACL 2025 Anthology 官方论文已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://aclanthology.org/2025.acl-long.1302/
overview_figure: ../assets/images/papers/lpoi-overview.png
overview_figure_source: Figure 2 from the official ACL 2025 paper
tags: [LPOI, Listwise preference, Object visibility, Visual prompting, ACL]
---

# LPOI

<div class="paper-meta"><span>ACL 2025</span><span>Training / Alignment</span><span>LoRA</span><span>已精读</span></div>

[论文原文](https://aclanthology.org/2025.acl-long.1302/){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>LPOI 不只比较一个正响应和一个负响应，而是逐步遮挡目标对象并形成可见度有序的图像列表，要求模型对正确对象描述的偏好随视觉证据增强而单调上升。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/lpoi-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/lpoi-overview.png" alt="LPOI 官方方法总览"></a><figcaption>官方方法概览图（论文 Figure 2）：从遮挡到原图的可见度序列与 listwise preference objective。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 核心问题 | pairwise DPO 只知道谁更好，不知道视觉证据变化的强弱顺序 |
| 数据 | 对目标对象做多级遮挡，必要时用红圈视觉提示引导关注遮挡区 |
| 目标 | DPO + anchor + listwise ranking，保持原图正确响应概率并学习单调顺序 |
| 模型 | LLaVA-v1.5 7B/13B、Idefics2-8B |
| 基准 | Object HalBench、MMHalBench、AMBER、HallusionBench |

## 2. 研究背景

普通 DPO 把视觉条件固定，只比较两个文本；即使模型依靠语言风格区分 chosen/rejected，也可能获得低 loss。LPOI 将视觉输入本身变成连续控制变量：目标越可见，正确对象描述应越可信。这提供比二元配对更丰富的监督，也更接近“视觉证据利用”的定义。

但遮挡不是天然反事实。周围上下文可能仍泄露对象，mask 纹理也可能成为捷径。论文增加视觉提示以让模型注意被操作区域，却同时改变图像分布；所以必须把视觉提示、遮挡程度、列表长度和非目标内容保持分别消融。

## 3. 方法详解

对图像中的目标对象生成由强遮挡到原图的多个版本，组成有序列表。相同正确响应在这些图像下应获得递增偏好。listwise loss 同时比较多个序位，较 pairwise 能利用全局次序；标准 DPO 维持 chosen/rejected 区分，anchor loss 保证原始图像的正确响应绝对概率不下降。

当遮挡后模型仍从背景推断对象时，作者以视觉提示突出被遮挡区域。总目标为 $L_{DPO}+L_{Anchor}+L_{Listwise}$，通过 LoRA 微调。列表越长，排序约束越丰富但训练成本也更高。

## 4. 实验设计

### 4.1 设置

训练数据取 Silkie preference 与 LLaVA-Instruct 子集，主规模 10K。LLaVA 训练 1 epoch，Idefics2 训练 3 epochs；并在单张 RTX A6000 的等 20 小时预算下重比 DPO、mDPO 与 LPOI。指标覆盖 CHAIR、MMHal score/HalRate、AMBER Cover/HalRate/Cog 和人类偏好。

### 4.2 主结果

| 模型 / 指标 | Base | LPOI | 解读 | 来源 |
|---|---:|---:|---|---|
| LLaVA-7B Object HalBench CHAIR$_S$/$_I$ ↓ | 原文基线较高 | 24.3 / 14.6 | 优于 mDPO 30.7 / 16.0 | Table 1 |
| LLaVA-13B CHAIR$_S$/$_I$ ↓ | 44.3 / 21.2 | 24.3 / 11.7 | 两项显著下降 | Table 1 |
| Idefics2-8B CHAIR$_S$/$_I$ ↓ | 6.3 / 4.2 | 5.3 / 3.6 | 强基线上仍有收益 | Table 1 |
| Idefics2 MMHal score/HalRate | 2.62 / 0.43 | 2.88 / 0.36 | 质量提高且幻觉下降 | Table 1 |
| Idefics2 AMBER CHAIR/HalRate ↓ | 3.4 / 7.6 | 2.6 / 5.7 | Cover 36.5→36.4，基本保持 | Table 1 |
| 等 20h 预算，Idefics2 CHAIR$_S$/$_I$ | 6.3 / 4.2 | 5.3 / 4.0 | 优于等时 DPO/mDPO | Table 2 |

跨三个主干的改善支持方法具有一定通用性。Idefics2 的 AMBER Cover 几乎不变，是比单独 CHAIR 更有价值的控制；LLaVA-7B 主表仍需联读输出质量和长度，避免把生成风格变化误作视觉 grounding。

### 4.3 消融与分析实验

视觉提示使 Idefics2 Object HalBench CHAIR$_S$/$_I$ 从 5.3/4.0 降至 5.0/3.4，MMHal score 从 2.74 升到 2.91；梯度 saliency 也更集中于遮挡区。列表长度 3→4→5 时 CHAIR$_S$ 7.3→6.7→5.3、CHAIR$_I$ 5.1→4.5→3.6，说明更细排序提供额外信号。人评中 LPOI 对 DPO/mDPO 更常获胜，Krippendorff α 为中到高一致。等训练时长对照削弱了“收益仅来自更多计算”的解释，但视觉提示与 mask 伪迹仍可能共同形成 shortcut。

## 5. 亮点与贡献

- 将二元视觉反事实扩展为可见度序列，监督信息更密集。
- 提供等 GPU 时长比较和列表长度消融。
- 在强基线 Idefics2 上同时保持 Cover、改善幻觉。

## 6. 局限

遮挡程度不等于真实世界证据强度，视觉提示进一步改变自然分布。列表需要可靠对象 mask，难扩展到抽象属性和关系。训练成本随列表长度增长。论文没有跨编辑器或自然目标缺失验证，也未证明单调排序在自由生成每个对象 token 上成立。

还需注意排序标签默认“对象越清晰，回答越应提及它”，但在开放描述中，显著性、用户问题和篇幅预算同样决定是否应该提及。一个低可见但与问题高度相关的对象可能比清晰背景对象更重要。因而 listwise 目标在描述任务与问答任务中的语义并不完全相同，复现时应分别报告，并检查模型是否把视觉提示的红圈当成新的指令 token。若 mask 边界或红圈颜色与训练标签固定相关，跨样式测试是最低限度的 shortcut control。

## 7. 与我的研究关系

LPOI 提供“证据剂量–响应曲线”的训练范式。可将对象删除图扩展为多级删除，并加入外观匹配 sham；若只有目标证据梯度而非 mask 强度能预测 token 变化，才更接近因果视觉利用。

## 8. 可执行的后续实验

1. 比较 mask、inpainting、自然遮挡三种可见度序列。
2. 加入非目标对象相同面积遮挡的 matched sham。
3. 对每级图像测目标 token logit、非目标 KL 和自由生成 mention rate。
4. 绘制列表长度–GPU 小时–CHAIR/Recall Pareto。
5. 在 description 与 targeted QA 两类 prompt 上分别验证排序单调性，并对红圈颜色、粗细和位置做样式置换。

## 9. 复现清单

- [x] 官方 Figure 2、主表、等时比较和列表消融已登记
- [ ] 固定对象 mask、遮挡算子、视觉提示样式
- [ ] 保存每级图像与排序标签
- [ ] 记录训练时长、显存、seed 和 LoRA 配置
- [ ] 同时报 Cover、长度、Recall 与人评协议

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 视觉证据 listwise preference |
| 证据强度 | 4/5 | 等时、列表、视觉提示与人评齐全 |
| 可复现性 | 3/5 | 数据构造细节和 mask 工具依赖较强 |
| 相关性 | 5/5 | 直接对应多级视觉反事实训练 |

## 11. 来源边界

本文依据 ACL 2025 Anthology 官方论文整理。数字来自 Tables 1–4 与人类评估；对 matched sham、自然遮挡和剂量响应的讨论属于本站分析。

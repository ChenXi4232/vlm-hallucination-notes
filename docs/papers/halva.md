---
title: "Mitigating Object Hallucination in MLLMs via Data-Augmented Phrase-Level Alignment"
description: HALVA 以对象短语级正负对和分布保持约束训练 LVLM，减少自由生成对象幻觉
authors: [Pritam Sarkar, Sayna Ebrahimi, Ali Etemad, Ahmad Beirami, Sercan Ö. Arık, Tomas Pfister]
venue: ICLR
year: 2025
resource_type: 方法论文
direction: Training / Alignment
hallucination_type: [Object hallucination, Free-form generation]
method_level: [Phrase-level, Training-level]
training: LoRA fine-tuning
status: 已精读
source_status: ICLR 2025 官方论文与官方代码已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://proceedings.iclr.cc/paper_files/paper/2025/hash/b73228d026ef49bfa49f95b7e330513e-Abstract-Conference.html
code_url: https://github.com/pritamqu/HALVA
overview_figure: ../assets/images/papers/halva-overview.png
overview_figure_source: Figure 4 from the official ICLR 2025 paper
tags: [HALVA, Phrase alignment, LoRA, CHAIR, AMBER, ICLR]
---

# HALVA

<div class="paper-meta"><span>ICLR 2025</span><span>Training / Alignment</span><span>LoRA</span><span>已精读</span></div>

[论文原文](https://proceedings.iclr.cc/paper_files/paper/2025/hash/b73228d026ef49bfa49f95b7e330513e-Abstract-Conference.html){ .kb-button .primary } [官方代码](https://github.com/pritamqu/HALVA){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>HALVA 将响应中的正确对象短语替换为可混淆的错误对象，直接在短语级拉开正确/幻觉 token 序列的似然，同时以 KL 项约束模型不要偏离原始能力。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/halva-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/halva-overview.png" alt="HALVA 官方方法总览"></a><figcaption>官方方法概览图（论文 Figure 4）：对象替换数据增强、短语级对齐损失与分布保持。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 研究对象 | 自由描述中生成图像不存在的对象 |
| 数据构造 | 定位正确对象短语，替换为语义或共现上易混淆的 hallucinated phrase |
| 目标 | 对每个正负短语对做直接偏好对齐，并以 KL 保持一般能力 |
| 模型 | LLaVA-v1.5 7B/13B、VILA 13B/384 |
| 评测 | CHAIR、AMBER、MME-Hallucination 与通用能力基准 |

## 2. 研究背景

句级偏好优化会把所有 token 共享一个标签，难以指出错误究竟发生在哪个实体；只做拒答或缩短输出又容易以 recall 为代价改善 CHAIR。HALVA 的核心判断是：object hallucination 通常可定位到局部 noun phrase，应把监督集中在最小错误跨度，同时对其余分布施加保持约束。

数据增强比采集整段人工偏好便宜，但也引入新的构念风险：替换对象可能语法不自然、与上下文不协调，模型可能学习语言捷径而不是视觉证据。因而覆盖率、长度、通用能力和真实自由生成评测缺一不可。

## 3. 方法详解

给定图像和正确响应，HALVA 识别其中对象短语，构造与图像不一致的替换短语。对正短语 $y^+$ 和负短语 $y^-$，loss 提升条件似然比，使模型在相同前缀和视觉条件下偏好正确实体。与整段 DPO 相比，未改动上下文不会反复贡献梯度，credit assignment 更局部。

第二项 KL regularization 让当前模型在正常样本上贴近参考模型，避免训练把所有对象词概率一并压低。基础 LVLM 以 LoRA 更新，部署时无需额外 forward、外部 detector 或改变 decoding。真正新增成本在离线对象抽取、负短语生成和微调。

## 4. 实验设计

### 4.1 设置

主实验覆盖 LLaVA-v1.5 7B/13B 与 VILA。自由生成用 COCO/CHAIR 和 AMBER，后者同时登记 coverage、hallucination rate 和认知错误；封闭式能力用 MME-Hallucination。对照包含原模型和多种解码/训练缓解方法，并检查长度与一般能力。

### 4.2 主结果

| 模型 / 指标 | Base | HALVA | 解读 | 来源 |
|---|---:|---:|---|---|
| LLaVA-1.5-7B CHAIR$_I$/CHAIR$_S$ ↓ | 15.4 / 50.0 | 11.7 / 41.4 | 实体级与句级均下降 | Table 1 |
| LLaVA-1.5-7B length | 100.6 | 92.2 | 有 8.4 token 缩短，需联读 recall | Table 1 |
| VILA-13B/384 CHAIR$_I$/CHAIR$_S$ ↓ | 9.2 / 33.0 | 8.4 / 30.0 | 跨架构收益较小但一致 | Table 1 |
| AMBER CHAIR / Cover ↑ | 7.8 / 51.0 | 6.6 / 53.0 | 幻觉下降且覆盖略升 | Table 3 |
| AMBER HallRate / discriminative F1 ↑ | 36.4 / 74.7 | 32.2 / 83.4 | 生成与判别均改善 | Table 3 |
| MME-Hall 7B ↑ | 648.3 | 665.0 | 封闭式幻觉能力提升 | 主结果表 |

结果比只报 CHAIR 更可信，因为 AMBER coverage 未随 hallucination 下降。LLaVA 的输出变短仍提醒我们：收益可能部分来自行为分布变化，应以逐样本内容保持继续审计。

### 4.3 消融与分析实验

论文比较 phrase-level alignment、分布保持项和数据增强组成。去掉局部短语对齐会弱化 hallucination 改善，去掉 KL 则更易损伤通用能力，说明二者分别承担“纠错”和“保持”。跨 7B/13B/VILA 的一致趋势支持不是单一 checkpoint 偶然现象；AMBER 中 Cover 51.0→53.0 是重要控制。但缺少“语法同样自然、仅视觉真值不同”的严格 matched negative，也未给每项改进的多 seed/置信区间，无法完全排除合成文本捷径。

## 5. 亮点与贡献

- 把句级偏好分解到可解释的错误对象短语。
- 部署时零额外 forward，适合作为训练型 baseline。
- 同时报 coverage、长度和通用能力，较好防止保守生成混淆。

## 6. 局限

对象替换质量决定监督上限；属性、关系与计数错误不一定能被 noun phrase 替换覆盖。训练负样本与真实模型自发错误的分布可能不一致。KL 只保证分布平均接近，不保证每个图像的正确对象 recall。若对象标注缺失，所谓负短语也可能真实存在。

## 7. 与我的研究关系

HALVA 是“局部反事实负例是否比整段偏好更有效”的直接参照。可把它与对象删除图配对：同一目标分别构造文本替换、图像删除和 matched sham，比较哪类干预真正增加视觉依赖、且不损伤非目标实体。

## 8. 可执行的后续实验

1. 以真实错误短语、随机替换、语义匹配替换做三路训练，隔离语言自然度。
2. 在等长度条件下比较 base/HALVA，联合报告 CHAIR、Recall、Cover 和 THRONE。
3. 对已删除对象与未删除对象分别测 token logit，检查模型是否学会利用视觉差异。
4. 用跨编辑器、自然缺失图像验证训练收益的迁移。

## 9. 复现清单

- [x] 官方 Figure 4、代码、主表与关键控制已登记
- [ ] 固定对象抽取器、替换候选和过滤阈值
- [ ] 记录 LoRA 配置、seed、训练样本去重
- [ ] 对合成负例做人类自然度与真实性抽检
- [ ] 同时报生成长度、Recall、Cover 与一般能力

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | phrase-level credit assignment 清晰 |
| 证据强度 | 4/5 | 多模型、多指标并含 coverage |
| 可复现性 | 4/5 | 官方代码已公开 |
| 相关性 | 5/5 | 直接对应对象级反事实训练 |

## 11. 来源边界

本文依据 ICLR 2025 官方论文和作者代码仓库整理。数字来自原文 Tables 1、3 及 MME 主结果；对 matched negative、编辑器迁移和视觉依赖的建议属于本站分析。

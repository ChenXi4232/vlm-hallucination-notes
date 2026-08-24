---
title: "Look Twice Before You Answer: Memory-Space Visual Retracing for Hallucination Mitigation in Multimodal Large Language Models"
description: MemVR 将视觉 token 视为 FFN 记忆，在中层不确定时动态重注入视觉表征
authors: [Xin Zou, Yizhou Wang, Yibo Yan, Yuanhuiyi Lyu, Kening Zheng, Sirui Huang, Junkai Chen, Peijie Jiang, Jia Liu, Chang Tang, Xuming Hu]
venue: ICML
year: 2025
resource_type: 方法论文
direction: Representation / Activation
hallucination_type: [Object hallucination, General multimodal hallucination]
method_level: [FFN-level, Dynamic routing]
training: Training-free inference
status: 已精读
source_status: ICML 2025 PMLR 论文与官方代码已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://proceedings.mlr.press/v267/zou25e.html
code_url: https://github.com/1zhou-Wang/MemVR
overview_figure: ../assets/images/papers/memvr-overview.png
overview_figure_source: Figure 1 from the official ICML 2025 paper
tags: [MemVR, Visual retracing, FFN memory, Dynamic intervention, ICML]
---

# MemVR

<div class="paper-meta"><span>ICML 2025</span><span>Representation / Activation</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://proceedings.mlr.press/v267/zou25e.html){ .kb-button .primary } [官方代码](https://github.com/1zhou-Wang/MemVR){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>MemVR 将投影后的视觉 token 当作可检索“记忆”，当中间层输出分布的不确定性超过阈值时，把视觉表征重新送入 FFN，从而在语言先验占优前进行一次动态 visual retracing。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/memvr-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/memvr-overview.png" alt="MemVR 官方方法概览"></a><figcaption>官方方法概览图（论文 Figure 1）：常规 MLLM 与中层视觉记忆重注入的对比。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 现象 | 随层数加深，生成越来越受语言模式驱动，早期视觉信息被稀释 |
| 触发 | 根据中间层 token distribution 的不确定性动态选择 retracing 层 |
| 干预 | 将视觉 embeddings 映射进 FFN memory space 并与当前状态融合 |
| 训练 | 冻结模型，无外部 detector 训练；需阈值与候选层配置 |
| 评测 | CHAIR、POPE、HallusionBench、MME、LLaVA-Bench |

## 2. 研究背景

视觉 token 通常只在输入阶段进入 decoder，随后经过多层自回归计算可能被语言先验覆盖。已有 contrastive decoding 重跑无图或扰动图，成本接近双 forward；静态 activation steering 又对所有样本一刀切。MemVR 的思路是利用模型内部不确定性决定“何时再看一次图像”。

论文借用 transformer FFN 可视作 key-value memory 的解释，把视觉 embeddings 变成额外 memory entries。该解释具有直觉，但并不等价于已经证明 FFN 存储明确对象事实；真正可检验的是动态重注入是否提高视觉依赖且不造成覆盖率、长度或通用能力退化。

## 3. 方法详解

在候选中间层计算当前 next-token distribution 的置信/熵指标。若风险超过阈值 $\gamma$，将初始视觉表示通过适配映射重注入该层 FFN，与原 hidden state 融合；若未触发则保持标准路径。动态策略只在需要时重追踪，静态版本则在固定层执行。

默认阈值约 0.75。层选择和阈值可能依数据集、模型与 prompt 改变，因此“training-free”只表示不更新权重，不表示无需 calibration。触发率、层分布和额外矩阵计算应计入真实成本。

## 4. 实验设计

### 4.1 设置

以 LLaVA 等主干在 COCO CHAIR、三套 POPE 数据、MME 和 HallusionBench 上比较 vanilla、对比解码与其他缓解方法。自由生成表报告 CHAIR$_S$/CHAIR$_I$、长度和 recall；通用能力由 LLaVA-Bench 等检查。

### 4.2 主结果

| 设置 / 指标 | Base | MemVR | 解读 | 来源 |
|---|---:|---:|---|---|
| LLaVA CHAIR$_S$/CHAIR$_I$ ↓ | 50.0 / 15.4 | 46.6 / 13.0 | 幻觉下降 | Table 3 |
| LLaVA length / Recall ↑ | 100.6 / 77.1 | 99.6 / 80.8 | 未靠缩短，recall 反升 | Table 3 |
| POPE COCO Avg Acc/F1 ↑ | 79.83 / 79.29 | 86.93 / 85.88 | 约 +6–7 pt | Table 4 |
| POPE A-OKVQA Avg Acc/F1 ↑ | 79.13 / 79.10 | 86.21 / 86.64 | 跨数据一致 | Table 4 |
| POPE GQA Avg Acc/F1 ↑ | 78.99 / 79.13 | 85.25 / 85.59 | 跨数据一致 | Table 4 |
| LLaVA-Bench Avg ↑ | 64.8 | 65.2 | 通用质量基本保持 | 主结果 |

CHAIR 中 recall 77.1→80.8 是关键控制，说明该配置不只是少报对象。POPE 的大幅收益仍需检查 yes/no calibration，而 HallusionBench 和通用基准的较小提升提示方法不是所有幻觉类型都同样有效。

### 4.3 消融与分析实验

论文比较静态与动态 retracing、不同候选层和阈值。动态触发总体优于固定早/晚层，说明视觉信息稀释的位置具有样本差异；$\gamma$ 扫描存在中间最优点，阈值过低导致过度注入、过高则很少触发。跨 benchmark 最佳层并不完全一致，这既支持动态路由，也暴露 calibration 敏感性。CHAIR 中长度近乎不变、Recall 上升构成有意义的行为控制；但论文缺少每样本 paired CI、严格 trigger-matched 随机层和自然图像分布外验证。

## 5. 亮点与贡献

- 将视觉重注入设计成条件触发，而非全程静态修改。
- 不需要第二个图像 forward，成本低于典型对比解码。
- 自由生成中同时改善 CHAIR 与 Recall，结果形态较健康。

## 6. 局限

“FFN 是视觉记忆”更像解释框架而非唯一机制。阈值需按模型/任务调整，可能发生 calibration overfit。重注入也可能只是增大视觉 token norm，不保证专门恢复目标对象证据。对属性、关系、计数和长文本漂移的覆盖弱于对象存在性。

## 7. 与我的研究关系

MemVR 可作为动态单 pass 干预 baseline，尤其适合检验“只在证据不足时介入”能否优于全局 steering。需要把触发分数与真正的对象可恢复性分开：高不确定不一定代表可由视觉补救，低不确定也可能是自信幻觉。

## 8. 可执行的后续实验

1. 比较 entropy trigger、对象证据 gap、随机同频 trigger 三种路由。
2. 在相同触发率下扫描层，报告 target/non-target token 的局部效应。
3. 记录每样本触发层、次数、延迟、CHAIR 与 Recall 的配对变化。
4. 用对象删除与 matched sham 判断重注入是否响应真实视觉差异。

## 9. 复现清单

- [x] 官方 Figure 1、代码、主结果和关键阈值分析已登记
- [ ] 固定模型版本、prompt、候选层和阈值选择 split
- [ ] 记录 trigger rate 与每 token 额外开销
- [ ] 加入同频随机触发与固定层对照
- [ ] 报告多 seed 或 bootstrap CI

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 动态 FFN 视觉重追踪 |
| 机制证据 | 3/5 | 分层分析充分但替代解释仍在 |
| 效率 | 4/5 | 单 forward 内增量计算 |
| 相关性 | 5/5 | 直接连接风险门控与视觉恢复 |

## 11. 来源边界

本文依据 ICML 2025 PMLR 官方论文及作者代码整理。数字来自原文 Tables 3–4 与通用能力结果；对触发构念、对象删除与 paired audit 的建议属于本站分析。

---
title: 实验笔记模板
tags:
  - Template
  - Experiment
---

# 实验笔记模板

## Research Question

一句话写出可证伪问题，避免只描述“测试某方法是否有效”。

## Hypothesis

- **H1**：
- **H0**：
- 可能的替代解释：

## Setup

| 项目 | 配置 |
|---|---|
| Model / checkpoint | |
| Dataset / split | |
| Prompt | |
| Decoding | |
| Seed | |
| Compute | |

## Intervention Matrix

| Condition | Changed variable | Controlled variables | Expected effect |
|---|---|---|---|
| Vanilla | — | — | |
| Counterfactual | | | |
| Targeted intervention | | | |
| Random control | | | |

## Recorded Outputs

- token、span、claim 与 hallucination label；
- top-k logits/probs/ranks 与 entropy；
- selected layer/head/MLP/KV activation；
- CHAIRi/CHAIRs、Recall/Coverage；
- length、repetition、max-length rate；
- runtime 与显存。

## Results

报告主表、置信区间、失败样例与 Pareto 曲线。

## Interpretation Boundary

哪些观察支持机制假设，哪些只能说明相关性？是否存在 detector、prompt、length 或 evaluator confound？

## Decision

- [ ] 扩大样本
- [ ] 增加 causal control
- [ ] 作为 baseline
- [ ] 停止路线
- [ ] 进入论文主实验


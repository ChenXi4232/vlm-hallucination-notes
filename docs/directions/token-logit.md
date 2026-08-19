---
title: Token / Logit 反事实
tags:
  - Token-level
  - Logit-level
  - Counterfactual
---

# Token / Logit 反事实

## 核心问题

在对象或属性 token 出现前，模型的候选分布是否真正随视觉输入变化？

$$
\Delta z_t(w)=z_t(w\mid I_{real},x,y_{<t})-z_t(w\mid I_{cf},x,y_{<t})
$$

其中 (I_{cf}) 可以是空白图像、无图分支、对象删除图、属性替换图或 mismatched image。不同反事实对应不同因果问题，不能混为统一的“language prior”。

## 关键阅读

- [M3ID](../papers/m3id.md)：有图/无图分布差异与 mutual-information decoding。
- [Self-Introspective Decoding](../papers/self-introspective-decoding.md)：基于 least-important visual tokens 的对比分支。
- [Curing Semantic Drift](../papers/curing-semantic-drift.md)：top-k candidates 的视觉重排与 selection failure。

## 最小实验记录

| 层面 | 必须保存 |
|---|---|
| Token | token id、字符跨度、对象 claim、hallucination label |
| Distribution | chosen logit/prob/rank、entropy、top-k candidates |
| Counterfactual | real/blank/no-image/edited image 的差分 |
| Quality | recall、coverage、caption length、循环率 |

!!! warning "解释边界"
    较大的 real-vs-blank logit gap 说明“输入条件改变了输出分布”，但不保证改变来自正确视觉证据；视觉编码器也可能稳定地读错属性或对象。


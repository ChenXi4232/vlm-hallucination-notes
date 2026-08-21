---
title: Dataset
tags:
  - Dataset
---

# Dataset

本页只按“数据在实验中承担什么角色”建索引；同一数据若同时用于训练与评测，必须在实验记录中显式区分 split，避免把评测标签泄漏到 detector/router 的选择过程。

## 当前常用数据角色

| 数据 | 在研究中的角色 | 风险 |
|---|---|---|
| MS COCO | caption、CHAIR、对象标注与反事实对象编辑 | 类别范围有限、同义词映射敏感 |
| POPE | 对象存在性判别与语言先验压力测试 | 模板化、不覆盖开放式详细回答 |
| Visual Genome | 属性、关系、region-level grounding | 标注噪声与长尾分布 |
| NoCaps | out-of-domain caption 泛化 | 对象覆盖和评测工具依赖 |
| AMBER data | 多类型生成/判别评测 | 需按版本核查标签与协议 |
| Visual CounterFact | 颜色/大小的 pixel–prior 反事实冲突与 steering | GPT-4o 筛选、SAM2 编辑伪影、仅两类属性 |
| CountBench-PIH | 对 baseline 计数正确样本施加 $N+k$ prompt 冲突 | 491 图规模小、任务定义依赖提示语义 |
| ROHE | MSCOCO 2017 对象移除后的成对存在性评测 | LaMa 伪影、人工筛选偏差、仅 object existence |
| SVO-Probes / MIT States / Facial Expressions | NOTICE 的 Semantic Image Pair 机制评测 | 自然配对背景差异与二选一任务简化 |

当前目录覆盖 27 篇 Notes 中反复出现的核心数据入口；新增论文若使用新数据集，应先补到这里，再在 benchmark 页补评测协议。

## 建议新增的数据视图

- 对象 token 与生成跨度对齐表；
- real/blank/no-image/counterfactual 图像对；
- safe onset 与 hallucination onset 窗口；
- 每个 claim 的 CHAIR label、POT/CLIP grounding 分数与内部 visual-dependence features。

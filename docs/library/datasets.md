---
title: Dataset
tags:
  - Dataset
---

# Dataset

## 当前常用数据角色

| 数据 | 在研究中的角色 | 风险 |
|---|---|---|
| MS COCO | caption、CHAIR、对象标注与反事实对象编辑 | 类别范围有限、同义词映射敏感 |
| POPE | 对象存在性判别与语言先验压力测试 | 模板化、不覆盖开放式详细回答 |
| Visual Genome | 属性、关系、region-level grounding | 标注噪声与长尾分布 |
| NoCaps | out-of-domain caption 泛化 | 对象覆盖和评测工具依赖 |
| AMBER data | 多类型生成/判别评测 | 需按版本核查标签与协议 |

## 建议新增的数据视图

- 对象 token 与生成跨度对齐表；
- real/blank/no-image/counterfactual 图像对；
- safe onset 与 hallucination onset 窗口；
- 每个 claim 的 CHAIR label、POT/CLIP grounding 分数与内部 visual-dependence features。


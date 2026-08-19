---
title: Evaluation / Recall Trade-off
tags:
  - Evaluation
  - Recall
  - CHAIR
  - POPE
---

# Evaluation / Recall Trade-off

## 基本审计矩阵

| 目标 | 推荐指标 | 主要漏洞 |
|---|---|---|
| 对象幻觉 | CHAIRi、CHAIRs | 对同义词映射和 COCO 类别覆盖敏感 |
| 对象存在性 | POPE Accuracy/F1/Yes-ratio | Yes/No 模板偏置，不代表开放生成 |
| 生成覆盖 | object recall / coverage | 依赖对象解析器和标注集合 |
| 文本质量 | length、repetition、distinct-n、人工检查 | 流畅不代表视觉忠实 |
| 检测器 | AUROC、AUPRC、Recall@Precision | 类别不平衡时 AUROC 可能过于乐观 |

## 最低报告要求

任何 mitigation 实验都应同时给出：

1. hallucination 指标；
2. object recall / coverage；
3. 平均生成长度与到达长度上限的比例；
4. 重复/循环率；
5. 至少一个通用能力或人工质量检查。

!!! danger "常见伪改进"
    更短、更保守或删除细节的回答经常降低 CHAIR，却没有增强视觉 grounding。若 recall 与 detailedness 同时下降，应把结论表述为 trade-off，而不是无条件缓解。


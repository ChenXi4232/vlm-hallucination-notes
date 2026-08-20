---
title: Benchmark 与 Metric
tags:
  - Benchmark
  - Metric
---

# Benchmark 与 Metric

本页是评测资产目录，记录“测什么、怎么报、哪里容易误读”。跨 benchmark 的最低实验报告规范与入口位于 [Benchmarks / Datasets](../benchmarks/index.md)，两页不复制论文列表。

## 核心评测表

| Benchmark | 形式 | 主要测量 | 必须补充的审计 |
|---|---|---|---|
| CHAIR | COCO caption | object hallucination | object recall、length、repetition |
| POPE | Yes/No QA | object existence | yes-ratio、三种负例采样 |
| AMBER | 生成 + 判别 | object/attribute/relation | 分类别结果与 coverage |
| MMHal-Bench | 开放回答 | 多类型幻觉 | judge 模型与提示敏感性 |
| SHR / HalluBench | sentence/word | 细粒度幻觉 | 标注一致性与 evaluator 误差 |

## 索引完整性

| 评测对象 | 已有入口 | 当前缺口 |
|---|---|---|
| Object caption | CHAIR | 同义词映射、length 与 recall 必须并报 |
| Object existence QA | POPE | random/popular/adversarial 与 yes-ratio 必须并报 |
| Attribute / relation | AMBER | 应按 existence/attribute/relation 分层 |
| Open-ended multi-type | MMHal-Bench | judge model、prompt 与版本必须冻结 |
| Token/sentence detection | SHR / HalluBench | 需报告类别基率、AUROC 与 AUPRC |

## Detector 指标

- **AUROC**：衡量整体排序能力，但类别极不平衡时可能看起来偏高。
- **AUPRC**：更关注正类稀少的检测场景，应与幻觉基率一起报告。
- **Recall@Precision**：适合部署阈值选择，直接反映漏检与误报权衡。
- **Bootstrap CI**：避免只报告单点 AUROC/AUPRC。

## 干预指标

建议始终输出一张 Pareto 表：CHAIRi/CHAIRs、Recall/Coverage、平均 tokens、循环率、长度上限触发率和通用能力。

---
title: Paper Card 模板
description: 面向 VLM hallucination 论文的可复现知识卡模板
tags:
  - Template
---

# Paper Card 模板

复制本页源码到 `docs/papers/<paper-slug>.md`，并替换以下 front matter：

```yaml
---
title: 完整论文标题
description: 一句话说明研究问题与方法
authors:
  - Author One
venue: CVPR
year: 2026
resource_type: 方法论文
direction: Attention Head / Path
hallucination_type:
  - Object hallucination
method_level:
  - Head-level
training: Training-free
status: 待读
source_status: 待核对
paper_url: https://...
code_url: https://...
tags:
  - Object hallucination
  - Attention head
  - Training-free
---
```

## 1. Basic Information

- **Title**：
- **Authors**：
- **Venue / Year**：
- **Paper / Code / Dataset**：
- **Main task**：
- **Model family**：

## 2. Problem Definition

说明 hallucination 类型、输入输出形式、任务设置，以及它与视觉依赖研究的关系。

## 3. Core Hypothesis

- 论文认为 hallucination 的直接原因是什么？
- 属于视觉编码、跨模态对齐、语言先验、解码选择、数据还是评测问题？
- 论文提供的是相关性证据还是因果证据？

## 4. Method Summary

按输入 → 中间模块 → 输出描述方法，并回答：

- 是否需要训练？
- 是否需要 detector、external model 或 human annotation？
- 干预发生在哪个 layer/head/token/decoding step？
- 需要缓存哪些激活或 logits？

## 5. Evaluation Details

| 项目 | 内容 |
|---|---|
| Dataset | |
| Benchmark | |
| Metric | |
| Baseline | |
| Model | |
| Ablation | |
| Main result | |
| Multi-seed / CI | |

## 6. Strengths

总结新颖性、实验扎实程度、机制价值和复现成本。

## 7. Weaknesses and Risks

检查指标漏洞、prompt bias、language-prior confound、annotation noise、外部 evaluator 依赖、error accumulation 与审稿风险。

## 8. Relevance to My Research

- 对 token/head/logit 反事实实验有什么启发？
- 能否支持 real image vs blank/counterfactual image？
- 作为 baseline、related work 或 motivation 的价值？
- 能否改造成低算力实验？

## 9. Possible Follow-up Experiments

每个实验填写：research question、model、data、intervention、recorded outputs、expected result、failure case、compute cost。

## 10. Comparison Tags

统一填写 training、detector、external evaluator、benchmark、interpretability、mitigation、baseline suitability 与 research relevance。


---
title: 深度论文笔记模板
description: 面向 VLM hallucination 论文的结构化精读、证据审计与实验转化模板
tags:
  - Template
  - Paper Note
---

# 深度论文笔记模板

本模板将原来的简略 Paper Card 升级为 **Deep Paper Note**。Front matter 负责检索与自动索引，正文负责还原方法、审计证据并转化为可执行研究设计。模板适用于方法论文；Survey、Benchmark 和 Dataset 可删去不适用的小节，但不得省略来源边界与局限。

!!! note "写作原则"
    先给读者结论，再解释方法；把论文声称、论文证据与个人推断分开；没有原文依据的数字、公式或因果结论一律标记为“待核对”。

## Front matter

复制本页源码到 `docs/papers/<paper-slug>.md`，替换以下字段：

```yaml
---
title: 完整论文标题
description: 一句话说明研究矛盾与核心方法
authors:
  - Author One
venue: CVPR
year: 2026
resource_type: 方法论文
direction: Attention Head / Path
secondary_directions:
  - Token / Logit
hallucination_type:
  - Object hallucination
method_level:
  - Head-level
training: Training-free
status: 已精读
source_status: 原文、补充材料与官方代码已核对
review_state: automated
arxiv_version: v1
last_verified: 2026-08-19
paper_url: https://...
openreview_url: https://...
code_url: https://...
overview_figure: ../assets/images/papers/<paper-slug>-overview.png
overview_figure_source: Figure N in the paper's official arXiv source package
tags:
  - Object hallucination
  - Attention head
  - Training-free
---
```

`review_state` 建议使用 `automated`、`user-reviewed` 或 `user-approved`；不要把 AI 精读自动标记为已人工复核。

`arxiv_version` 与 `last_verified` 用来冻结本次精读所依据的版本和核对日期；若不存在公开评审或官方代码，不要制造空链接，在正文“来源边界”中写明检索日期与“未发现”。

## 页面开头

```markdown
# 论文标题

<div class="paper-meta"><span>CVPR 2026</span><span>方法论文</span><span>Head-level</span><span>Training-free</span></div>

[论文原文](...){ .kb-button .primary } [OpenReview](...){ .kb-button } [官方代码](...){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>用一到两句交代研究矛盾、关键机制、方法和最重要结论。</p></div>
```

## 官方方法概览图

优先从论文官方 PDF 或 arXiv LaTeX source package 提取 pipeline / framework / method overview；不要使用博客重绘图替代论文原图。图片放在 `docs/assets/images/papers/`，并用下列结构记录图号、出处、版本与用途：

```html
<figure class="paper-figure">
  <a href="../../assets/images/papers/<paper-slug>-overview.png" target="_blank" rel="noopener">
    <img src="../../assets/images/papers/<paper-slug>-overview.png" alt="论文方法总览：简述图中流程">
  </a>
  <figcaption>官方方法总览（论文 Figure N）。图片提取自 <a href="https://arxiv.org/abs/...">arXiv v1</a> 的官方 LaTeX source package；点击查看原图。</figcaption>
</figure>
```

正文必须解释图中的输入、关键中间量、分支条件、干预位置与输出，不能只贴图。若论文没有方法图，明确写“官方版本未提供方法总览图”，再用 Mermaid 给出**本站等价抽象**，避免让读者误认作作者原图。

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 研究对象 | hallucination 类型与任务形式 |
| 核心归因 | visual encoding / alignment / language prior / decoding / evaluation |
| 方法类型 | training-time / inference-time / evaluation-only |
| 干预位置 | token / head / residual / logit / decoding path |
| 外部依赖 | detector、CLIP、LLM evaluator、human annotation |
| 主要评测 | dataset、benchmark、metric |
| 最适合角色 | baseline / related work / mechanism inspiration |

## 2. 研究背景与核心矛盾

### 2.1 研究的 hallucination

说明输入、输出、标签粒度和 benchmark 实际测量的错误，不要把 object hallucination 的结论直接外推到 attribute、relation 或 reasoning hallucination。

### 2.2 现有方法的缺口

说明论文针对的真实缺口，以及它是否只是换了一个 proxy 或 benchmark。

### 2.3 核心假设与证据强度

| 假设 | 论文证据 | 证据类型 | 仍可能的混淆因素 |
|---|---|---|---|
| H1 | | correlation / intervention / counterfactual | |

明确区分：相关性观察、组件消融、反事实干预和可跨模型复现的因果证据。

## 3. 方法详解

### 3.1 整体流程

优先给出简洁 Mermaid 流程图，随后按输入 → 中间量 → 决策/干预 → 输出解释。

### 3.2 关键量与公式

每个公式必须解释所有符号、张量维度、计算位置和直观意义。若为便于比较而写成统一形式，应标注“等价抽象”而非冒充论文原式。

### 3.3 实现细节

说明 layer/head/token selection、超参数、额外 forward、KV cache、beam search、外部模型以及时间/显存开销。

### 3.4 方法究竟改变了什么

说明它改变的是视觉依赖、语言先验、候选排序、生成长度还是回答倾向，并列出需要额外实验才能排除的替代解释。

## 4. 实验设计与关键结果

### 4.1 设置

| 项目 | 内容 |
|---|---|
| Models | |
| Datasets / splits | |
| Benchmarks | |
| Metrics | |
| Baselines | |
| Ablations | |
| Statistical evidence | seed、CI、显著性检验 |

### 4.2 主结果

只摘录支持核心论断的关键表格，并注明表号、指标方向、模型、数据集、对照方法与设置；不确定数字不要填写。至少保留一个可追溯的定量结果表，并检查正文数字与表格是否一致。

### 4.3 Ablation 与机制证据

检查随机 head/token 对照、强度扫描、跨数据迁移、输出长度、coverage/recall 和通用能力。

### 4.4 结果应该如何解读

分别写“论文能够支持什么”和“论文不能据此证明什么”。

## 5. 亮点与贡献

从问题重构、方法新颖性、证据质量、可复现性和机制价值分析，不重复摘要。

## 6. 局限、指标漏洞与审稿风险

至少检查：proxy validity、prompt bias、language-prior confound、annotation noise、external evaluator、length/recall trade-off、error accumulation、跨模型迁移和计算成本。

## 7. 与我的研究关系

### 7.1 可直接借鉴

连接 real vs blank/counterfactual image、token-level logits、head output、residual stream、logit lens、VR/PD/RBC/POT 等当前实验。

### 7.2 Baseline 决策

给出 high / medium / low，并解释复现成本、对比公平性和最小实现。

### 7.3 与已有路线的差异

说明该方法是直接证据、互补 proxy，还是可能与当前路线发生循环定义。

## 8. 可执行的后续实验

| 实验 | Research question | Model / data | Intervention / comparison | Recorded outputs | Expected observation | Failure case | Cost |
|---|---|---|---|---|---|---|---|
| E1 | | | | | | | Low |

## 9. 复现清单

- [ ] 原文与补充材料版本已记录
- [ ] 官方代码与 commit 已记录
- [ ] prompt、split、seed 与 generation config 已记录
- [ ] 主要指标可由公开脚本复算
- [ ] 同时记录输出长度、coverage / recall 与通用能力
- [ ] 外部 evaluator 的版本和 prompt 已冻结

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 新颖性 | | |
| 机制证据 | | |
| 实验完整性 | | |
| 可复现性 | | |
| 与当前研究相关性 | | |

## 11. 检索标签与来源边界

列出 requires training、inference-only、detector、external evaluator、interpretability、mitigation、baseline suitability。最后明确哪些内容来自原文，哪些是作者公开材料，哪些是个人分析，哪些仍待核对，并逐项登记：

- 核对的 arXiv / proceedings 版本与日期；
- 官方代码仓库与 commit（若尚未发布则写“截至日期未发现”）；
- OpenReview / 公开评审状态（不要把无搜索结果写成“没有评审”，应写“截至日期未发现公开页面”）；
- 方法图的原始文件、论文图号和提取来源；
- 数字冲突、正文—表格不一致或版本缺口。

---
title: "2026-10-10：CVPR精读与ICML正式卷扫描"
description: 两篇CVPR主会精读、ICML 2026正式卷候选池与CVPR 2027投稿政策核验
tags: [Reading Notes, CVPR, ICML, Evidence audit]
---

# 2026-10-10：CVPR精读与ICML正式卷扫描

本轮新增[HulluEdit](../papers/hulluedit.md)与[AdaIAT](../papers/adaiat.md)两篇CVPR 2026主会Deep Paper Notes，41→43篇。检查从main `b6d2938`开始；两篇均完整核对CVF正文、独立补充材料、arXiv v1与官方代码，`review_state: automated`，未执行复现实验。既有Note的`added_at`没有改写。

## 最值得借鉴的证据与审稿风险

- **HulluEdit**：LLaVA-1.5 greedy的CHAIRs 20.40→13.00、CHAIRi 7.08→4.18，同时BLEU 15.72→15.49；但补充材料中Qwen2.5 Recall 46.0→45.2、InternVL Recall 51.6→50.9。其“视觉分量不变”只对方法定义的低秩投影成立，不证明全部真实视觉语义无损。正文Eq. 17是硬门控，发布代码却使用连续λ、截断、PCR阈值、norm restoration与`blend_tau`，复现前必须冻结实现版本。
- **AdaIAT**：LLaVA-1.5-7B的CHAIRs 49.0→31.4、CHAIRi 13.3→8.3、F1 77.9→79.4、Distinct-1保持0.60；但固定IAT把层范围扩到5–31时CHAIRs可降至1.1，F1却崩到30.3，说明“更低幻觉率”可由抑制输出获得。方法不更新参数但并非零数据：逐层阈值和逐头幅度来自1万张COCO caption的真实/幻觉对象标签；token位置、对象重复、prefix质量和同域校准仍是关键替代解释。
- **CVPR投稿层面的共同启示**：主表必须与Recall/F1、长度、重复和通用能力同报；机制证据至少需要位置/重复匹配、随机层/随机子空间、同预算baseline、跨模型阈值迁移及失败案例。以上是本站基于证据的建议，不是官方录用保证，也不涉及任何个人未公开投稿方案。

## 官方会议、论文集与CCF状态

核验日期为2026-10-10；只把正式paper page或online-first视为系统扫描触发事件。首次观察日期不冒充真实发布日期。

| 来源 | 官方状态 | 本轮处理 |
|---|---|---|
| [CCF第七版目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/) / [AI类别](https://www.ccf.org.cn/Academic_Evaluation/AI/) | 第七版于2026-03-31正式发布；官方目录说明只认Full/Regular，排除Findings/Workshop。AI页可核对CVPR、ICCV、AAAI、NeurIPS、ACL、ICML等A级来源 | 两篇由CVF BibTeX确认是CVPR 2026主会；Findings与Workshop保持分轨，不借主会等级 |
| [CVPR 2026 CVF索引](https://openaccess.thecvf.com/CVPR2026?day=all) | CVF索引记录Main Conference于2026-05-23发布，Workshops为05-26，Findings为05-27 | 修正旧账本中“真实上线日UNKNOWN”；本轮继续历史补齐，不声称是本周新发布 |
| [ICML 2026 PMLR 306](https://proceedings.mlr.press/v306/) | 2026-09-29正式发布，共6,552条正式paper pages | 新release事件；完成全卷标题扫描与19篇直接VLM/MLLM幻觉摘要审查，未声称全文穷尽 |
| [NeurIPS 2026 Dates](https://neurips.cc/Conferences/2026/Dates) / [Proceedings](https://papers.nips.cc/) | 录用通知09-24、accepted papers导入10-04；正式proceedings索引最新仍为2025 | 通知与系统导入不算正式论文集发布；保留待核对 |
| [ACL 2026 Anthology](https://aclanthology.org/events/acl-2026/) | 正式论文集可访问 | 无新release-batch证据；不重复全量扫描 |
| [EMNLP Anthology venue](https://aclanthology.org/venues/emnlp/) | 官方venue索引当前只列至2025 | EMNLP 2026候选继续标“待正式paper page”，不猜发布日期 |

本轮只核对与当前候选和临近发布窗口直接相关的权威来源，不宣称已穷尽全部A级会议、期刊或online-first条目。

## CVPR 2027官方投稿政策快照

[官方CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)的日期与上轮相比未变：Registration 2026-11-10、Full paper 11-16、Supplementary 11-23，均为AoE；Reviews 2027-01-25，Rebuttal 01-25至02-01，Final decisions 02-25。OpenReview的[Complete Your Profile](https://cvpr.thecvf.com/Conferences/2027/CompleteProfile)页新增或明确强调：所有作者/审稿角色须有完整profile，registration截止后不得增删作者，任一作者注册不完整可能desk reject。

截至核验日，官网导航仍未独立发布2027 Author Guidelines与Reviewer Guidelines；不沿用2026版本填补空白。CFP仍将LLM政策标为待定，并将2026-09-15之后公开的工作一般视为contemporaneous，但仍要求引用、讨论及在可行时比较。会议计划在开会前两周公开录用论文，这是未来安排，不是当前proceedings release。

## 候选、评分与处置

评分顺序为**直接相关性/方法或理论新颖性/机制证据/实验完整性/复现与低算力/知识库新增信息**（1–5）。只有两篇完成全文、补充与代码核验后入选，其余评分是保守初筛。

| 候选 | 评分 | 处置与理由 |
|---|---|---|
| HulluEdit（CVPR 2026 main） | 5/4/3/4/3/5 | 入选；补上在线逐token正交子空间编辑，并公开记录召回损失、SVD记号与代码门控差异 |
| AdaIAT（CVPR 2026 main） | 5/4/3/4/3/5 | 入选；补上“历史文本是视觉证据载体”的注意路线，并揭示离线监督、位置混淆与崩坏消融 |
| Beyond the Global Scores（CVPR 2026 main） | 5/3/2/2/3/4 | P1延后；patch/token detector的held-out迁移、对象标签与位置混淆需全文核对 |
| Reallocating Attention Across Layers（CVPR 2026 main） | 4/3/2/2/3/4 | P2延后；需同预算延迟、随机层/随机头及感知—推理头定义审计 |
| CORAL v2（作者称NeurIPS 2026） | 5/4/2/2/3/5 | P1理论候选；正式decision、FDR假设、视觉扰动对称性和对象依赖尚待核对 |
| GHOST-Q（预印本） | 4/3/2/2/3/4 | P2；量化配对与generation budget尚未精读，不用摘要替代证据 |

### ICML 2026 release-batch

全卷标题扫描得到49个含`hallucin`的原始命中；阅读全文摘要后，19篇直接涉及VLM/MLLM视觉幻觉、忠实度或其缓解。49不是合格论文数，且窄关键词仍可能漏掉标题不显式写hallucination的机制论文。本轮两篇名额已用于CVPR补齐，ICML不降门槛凑数。

P1依次为HaloProbe、Causal Route Gating、Token-Level Visual-Sensitivity Steering、Inter-Layer Visual Attention Discrepancy、RUDDER、Beyond Blind Noising/DVR；P2为MM-Snowball与DOUBT。优先顺序依据：是否补充现有token/head/residual路线、能否审计混淆、代码/评审可得性和低算力复现价值。正式URL与下一步证据闸门已写入[待读队列](../library/reading-queue.md)。其余11篇保留在JSON游标，不在未精读前扩写主站结论。

## 分类、组件与索引

新增两篇分别落入既有`Attention head / path intervention`与`Representation / activation editing`，没有形成至少3篇无法表达的稳定新族，也未出现至少5篇同类歧义。本月结构审计已于10月3日执行；总数仅增加2篇，未达到“新增至少10篇”触发条件，因此不重构taxonomy、不新增UI组件。

本轮只做可回滚的信息架构维护：两篇接入Paper索引、首页最近接入、方法目录、方向页、研究版图、CVPR问题—证据矩阵；ICML扫描接入ML venue页和阅读队列。关系只标注共享问题、基线或本站比较，不虚构作者互引。

## 证据边界与验证

公开评审不是收录硬条件。截至2026-10-10未发现两篇CVPR论文可引用的公开评审页面，故Note不写reviewer concern或author response。HulluEdit与AdaIAT均未由本站复现实验，硬件时延、跨模板token边界、数据划分和论文—代码差异仍需人工复核。

提交前执行确定性索引生成、Deep Paper Note校验、公开边界检查、`mkdocs build --strict`与HTML链接验证；实际结果和发布状态以本轮PR及GitHub Pages工作流为准。扫描恢复信息见[JSON账本](research-atlas-scan-20261010.json)。

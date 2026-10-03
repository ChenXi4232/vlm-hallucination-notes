---
title: "2026-10-03：CVPR补齐与来源核验"
description: CVPR主会筛选、两篇精读、投稿政策与公开证据缺口
tags: [Reading Notes, CVPR, Evidence audit]
---

# 2026-10-03：CVPR补齐与来源核验

本轮新增[PTI](../papers/prefill-time-intervention.md)与[FLB](../papers/first-logit-boosting.md)两篇CVPR 2026主会Deep Paper Notes，39→41篇。检查基于main `950ee5d`；未覆盖任何并行PR，检查时无open PR。旧Note的added_at保持原值。

## 最值得保留的证据

- PTI Table 1：LLaVA greedy CHAIRs 47.4→15.4；但Table 5 F1 75.3→72.7，Supplement Figure 6平均长度98.9→79.5。降低幻觉不能等同于保召回。
- FLB Table 2：LLaVA CHAIRs 57.5→43.5、Recall73.3→73.6；Supplement Table 16的greedy AMBER Cover50.5→48.8。Table 5 The-only消融说明语言形式是重要替代解释。
- 两篇都已读CVF正文、独立supplement与官方核心代码；均未执行复现实验，review_state=automated。公开评审不是硬门槛，截至检查日未发现可引用的公开评审页面；没有虚构审稿人意见或作者回复。

## 官方会议/论文集状态

检查日期均为2026-10-03。HTTP不可访问不等于未发布；首次观察公开不等于实际发布日期。以下是本轮实际核验范围，不宣称覆盖全部CCF会议与期刊。

| 来源 | 实际观察 | 发布/扫描处理 |
|---|---|---|
| [CVPR 2026 CVF主会](https://openaccess.thecvf.com/CVPR2026?day=all) | 可读取4042个标题条目与正式paper pages | 完整目录可访问，真实上线日UNKNOWN；本轮做历史补齐，不谎称本周新发布 |
| [CVPR 2025主会](https://openaccess.thecvf.com/CVPR2025?day=all) | 2871标题条目 | 题目关键词筛选完成；尚未全量摘要审查 |
| [CVPR 2024主会](https://openaccess.thecvf.com/CVPR2024?day=all) | 2716标题条目 | 同上；Workshop未混入 |
| [ICCV 2025 CVF](https://openaccess.thecvf.com/ICCV2025?day=all) | 目录HTTP200、正式条目可读 | 本轮仅核验可用性，没有新增release事件证据 |
| [ICML 2026官方paper目录](https://icml.cc/virtual/2026/papers.html) / [PMLR](https://proceedings.mlr.press/) | 前者可读；PMLR当前索引未列ICML2026正式卷 | paper pages与正式出版卷分开；真实发布日期未知，未做全量批次扫描 |
| [ACL 2026](https://aclanthology.org/events/acl-2026/) | 返回大型目录，检索器因体积过大未展开 | 保留公开可访问证据，不推定本周新增 |
| [NeurIPS 2026日期](https://neurips.cc/Conferences/2026/Dates) / [paper目录](https://neurips.cc/virtual/2026/papers.html) | 通知日为9月24日AoE；目录403 | 录用通知不作为论文集发布；正式公开批次待核对 |
| [EMNLP 2026 Anthology入口](https://aclanthology.org/events/emnlp-2026/) | 404 | 本入口尚不可用，不能推断所有accepted/program页面都不存在 |
| [AAAI proceedings archive](https://ojs.aaai.org/index.php/AAAI/issue/archive) | 502 | 暂时检索失败；不记为尚未出版，下轮重查 |

**CCF边界**：[当前目录说明](https://www.ccf.org.cn/Academic_Evaluation/By_category/)的官方搜索索引包含2026年3月调整公示与“Full/Regular paper，排除Findings/Workshop”等说明；[AI类别页](https://www.ccf.org.cn/Academic_Evaluation/AI/)的官方索引可核对CVPR、ICCV、AAAI、NeurIPS、ACL、ICML及AI/TPAMI/IJCV/JMLR。直接页面返回验证，且类别页索引仍含可能属于旧版本的IJCAI条目，不能断言已完整核验第七版的所有升降级。本轮不采用第三方博客推定ICLR/IJCAI等变更，最新完整等级表仍为待核对。CVPR两篇的主会身份由CVF正式BibTeX独立确认。

期刊采用逐篇online-first监测，不以卷期日期代替单篇公开日期。本轮未完成所有期刊的增量核验；此缺口不写成“没有新论文”。

## CVPR 2027 官方政策快照

[官网](https://cvpr.thecvf.com/Conferences/2027)显示9月3日发布CFP入口；[日期页](https://cvpr.thecvf.com/Conferences/2027/Dates)与[CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)共同列出：

| 事件 | 官方日期 / 时区 |
|---|---|
| Paper Registration（不要擅自改称全文） | 2026-11-10，AoE（UTC−12） |
| Full-paper submission | 2026-11-16，AoE |
| Supplementary | 2026-11-23，AoE |
| Reviews released | 2027-01-25，AoE |
| Rebuttal | 2027-01-25至02-01，AoE |
| Final decisions | 2027-02-25，AoE |

CFP称2026-09-15之后上线的工作一般按contemporaneous处理，但仍要求引用讨论、在可行范围内比较；不能理解为可以忽略。LLM使用政策仍在制定。CFP所链[Author Guidelines](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines)返回404，[Reviewer Guidelines](https://cvpr.thecvf.com/Conferences/2027/ReviewerGuidelines)未能获取，独立指南内容记为未核实，不沿用往届。CFP所说会前两周公开论文是未来政策，不是已经发生的release。

## 候选与取舍

共深入筛选8个候选（6个CVPR2026摘要、2个近期arXiv候选）；2篇精读、6篇延后。以下评分顺序为**相关性/新颖性/机制证据/实验完整性/复现与低算力/新增信息**。未全文精读项为保守的初筛评分，不将摘要声称当成已验证结果。

| 候选 | 1–5评分 | 决策与可核验理由 |
|---|---|---|
| PTI | 5/4/3/4/4/5 | 入选；正文/补充/代码齐全，补上prefill KV维度；Table5有明确权衡 |
| FLB | 5/3/3/4/4/5 | 入选；核心实现成本低，Table5/19可分离语言偏置与截断 |
| [AdaIAT](https://arxiv.org/abs/2603.04908) | 5/4/2/2/3/4 | P1待读；CVF摘要提出增强生成文本attention而非只增强图像，值得检验重复/recall；正文未本轮全读 |
| [HulluEdit](https://arxiv.org/abs/2602.22727) | 5/4/2/2/3/4 | P1待读；摘要声称正交子空间保护视觉分量，需核对投影假设与真实grounding是否同一概念 |
| [Beyond the Global Scores](https://arxiv.org/abs/2604.04863) | 5/3/2/2/3/4 | P1待读；patch-level检测需审计位置/对象标签混淆与held-out迁移 |
| [Reallocating Attention Across Layers](https://arxiv.org/abs/2510.10285) | 4/3/2/2/3/4 | P2待读；CVF摘要聚焦感知/推理头重分配，延迟、计算量口径需要原文核对 |
| [CORAL](https://arxiv.org/abs/2609.38979v2) | 5/4/2/2/3/5 | P1理论候选；v2为2026-10-01，作者注明NeurIPS2026录用，官方decision未独立核验；需读mirror统计的对称性/依赖假设，不能先写成无条件FDR保证 |
| [GHOST-Q](https://arxiv.org/abs/2609.29999) | 4/3/2/2/3/4 | P2评测候选；9月24日预印本，摘要强调量化后同分数掩盖grounding变化；正文访问未完成，不能晋升精读 |

## 扫描覆盖与恢复规则

对三届主会**全部标题条目**执行 `hallucin / faithful / language prior` 字符筛选，2026/2025/2024分别命中48/22/12条。命中包括无关的3D生成和图像编辑，也包括已收录论文；82是原始题目命中数，不是82篇合格候选。该窄关键词扫描会漏掉不含这些词的grounding/机制工作，后续需扩大语义筛选。

2026本轮读取6篇正式摘要、其中2篇全文；2025/2024仅保存题目级游标，尚未全量读摘要。Nullu、HalLoc、VCD、HallusionBench等历史缺口保留到后续筛选，不伪称已补齐近三届。完整命中、正式URL和Note去重快照见[扫描记录JSON](research-atlas-scan-20261003.json)。

仓库未发现可确认的旧成功cutoff文件；不能把上次commit日期直接当成全流程成功时间。因此本轮按首次可恢复记录回看2026-09-03至10-03，并做CVPR历史补齐。JSON仅保存proposed cutoff，发布前不推进成功checkpoint。恢复时用分支对应PR、merge SHA及Pages工作流共同确认；若PR或部署失败，只恢复该阶段，不重复创建Notes。精读编号、slug、added_at均固定。

## 分类与界面审计

原39篇front matter含6种primary direction、10种venue值。方法层级存在自由文本变体；external_dependency/evidence_type/benchmark/baseline_suitability未形成统一字段，不能从缺字段推断论文缺实验。训练/推理和图文依赖从Note正文补充比较，UNKNOWN保持未知。

本轮两篇可放入既有logit editing与representation/KV类别，未形成3篇无法表达的新方法族，也未证明5篇同类歧义已妨碍检索，故不迁移taxonomy、不改兼容标签。首次10月审计只补充已有视觉会议页中的静态问题—方法—证据矩阵，不引入JS或新依赖；不声称已做新的全站移动端/键盘交互测试。其余调整为Notes连入现有目录、首页、研究版图、方向页。后续若要做多维筛选，应先以原文填充缺少的元数据，不能自动制造关系。

## 验证与发布证据位置

提交前要求索引生成、Deep Note校验、公开边界检查、strict构建及HTML链接验证通过；具体结果随本轮PR登记。本站页面不会预先声明已经发布，合并与部署以GitHub实际状态为准。待处理风险：CCF最新完整表、独立2027指南、公开评审与两篇复现实验配置缺口。未包含任何个人未公开研究计划或数据。

---
title: 2026-10-17：CVPR head-output审计与NeurIPS论文页批次
description: 一篇CVPR主会精读、候选分级、版本提醒与可恢复的公开扫描记录
tags: [Literature audit, CVPR, NeurIPS, Evidence boundary]
---

# 2026-10-17 来源核验

本轮从`main`的43篇Notes继续，新增1篇[Reallocating Attention](../papers/reallocating-attention.md)，总数44；没有为了用满名额把摘要升级为精读。所有新增分析标记`automated`，未运行模型实验。上轮PR #16已合并，合并SHA `ce3bfffd0cf807ce0f7332f323a1acd141dbfdd7`对应[Pages工作流](https://github.com/ChenXi4232/vlm-hallucination-notes/actions/runs/38013663820)成功，故本轮增量cutoff为2026-10-10；历史CVPR补齐不受此时间窗限制。

## 1. CVPR补齐：最有用的证据与风险

Reallocating Attention核对了CVF正文11页、独立补充16页，并复查主表、线性论证和归因公式的页面图像。arXiv元数据确认最新为2510.10285v3，2026-03-07。CVF下载入口本轮403，使用保留的公开PDF副本；不把访问失败当作论文不存在。

| 可追溯证据 | 读者应保留的边界 |
|---|---|
| Kimi HallusionBench Acc：64.76→68.19；Ocean-R1：49.41→53.64，正文Table 1 | 是最终答案任务分数，不是caption对象Recall |
| R1-Onevision MathVision：Vanilla33.54、仅感知33.90、仅推理29.63、联合39.12，Table 2 | 有交互，不证明视觉mass分型唯一正确；需要同层同数随机头 |
| Supplement Table 2：HallusionBench 101→103秒 | 不宜把同为二次复杂度宣传成零墙钟开销 |
| Supplement B Eq.14–15与H Eq.34–35 | 只增强正收益需要增强组本身有益的额外条件；输出投影后reshape不自动恢复真实head |

正文Table 1/2的Ocean MathVision Full（26.01/25.68）及Kimi SEED F1（53.62/53.64）不同，已逐表登记，不选有利值或重算统一均分。作者、题名、venue与版本不存在阻断元数据冲突；数字冲突不承担主结论证据。官方实现commit未定位。OpenReview检索能看到CVPR元数据，但未取得可引用的review/rebuttal/decision正文；旧ICLR withdrawn记录不自动当作本版评审。没有把自动摘要站当成独立权威评价。

## 2. 论文集与政策核验（2026-10-17）

等级依据[CCF第七版正式发布页](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)（2026-03-31；公告注明4月9日勘误）与[官方AI类别页](https://www.ccf.org.cn/Academic_Evaluation/AI/)。后者可检索核实AAAI、NeurIPS、ACL、CVPR、ICCV、ICML；最新完整PDF逐项覆盖仍待补齐，不用第三方名单推定其他venue等级。Full/Regular、Findings、Workshop不混同。期刊在线优先与卷期日期分开。

| Venue / 官方来源 | 本轮状态与日期证据 | 扫描处理 |
|---|---|---|
| [CVPR 2026 CVF](https://openaccess.thecvf.com/CVPR2026?day=all) | 正式主会paper pages可检索，正文/补充部分直连403。既有账本的2026-05-23发布日期本轮未获得新的原始公告复核 | 保留旧日期及其来源，不以本轮访问日期覆盖；新增1篇，另补2个标题/摘要候选；不称全量语义扫描 |
| [ICML / PMLR306](https://proceedings.mlr.press/v306/) | 官方卷说明2026-09-29发布 | 沿用已扫描6,552标题/19直接摘要的游标，不重复伪造新release |
| [NeurIPS Downloads](https://neurips.cc/Downloads/2026) / [proceedings](https://papers.nips.cc/) | 官方Downloads出现2026题名与论文event入口；正式proceedings索引仍未列2026。真实公开日期未知，本账本首次观察2026-10-17 | **官方论文页批次扫描**，不把09-24通知当发布日期；保存原始命中与待全文队列 |
| [ACL 2026](https://aclanthology.org/events/acl-2026/) | Anthology正式卷可见，long papers2223；会议日期07-02至07-07不是实际上线日期 | 未发现可确证的新批次；无本轮全量重扫 |
| [EMNLP](https://aclanthology.org/venues/emnlp/) | 官方venue索引最新列2025 | 2026正式paper page待核对；不从缺少条目推定从未公开 |
| [AAAI 2026](https://aaai.org/proceeding/aaai-40-2026/) | 官方说明48期；[Vol40 No2](https://ojs.aaai.org/index.php/AAAI/issue/view/684)标2026-03-17 | 单期日期不外推整套实际发布日；不属本周新release |
| [ICCV 2025](https://openaccess.thecvf.com/ICCV2025) | 既有正式索引可检索；实际公开日期本轮未知 | 历史库，不触发本周批次 |
| [JMLR Vol27](https://jmlr.org/papers/v27/) | 2026卷可读；与TMLR是不同刊物 | 未完成本周逐文日期审计，不声称无新相关论文 |
| [IJCV online-first](https://link.springer.com/journal/11263/online-first) | 返回异常陈旧的2009条目，不足以证明2026最新状态 | 数据缺口；TPAMI/AI等连续出版来源也未完成本周逐文日期核验，不推进覆盖游标 |

[CVPR 2027 CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)与[Dates](https://cvpr.thecvf.com/Conferences/2027/Dates)核对：Enrollment / Full / Supplement仍为2026-11-10 / 11-16 / 11-23，均AoE；本轮日期无变化。独立AuthorGuidelines入口404，ReviewerGuidelines未取得有效页面；不沿用2026指南冒充2027。CFP的LLM使用范围仍待公布。另明确记录：CFP将2026-09-15之后上线论文一般视为contemporaneous，但仍要求引用讨论、可行时实证比较，影响过投稿的工作仍须作为prior work引用；不是“不用比较”的豁免。该条是本轮补录，未证实网站何日新增。

## 3. 候选质量闸门

分数依次为：直接相关性 / 新颖性 / 机制证据 / 实验完整性 / 可复现低算力 / 知识库新增信息（1–5）。**仅摘要候选的证据、实验与复现分数保守记1，表示尚未核验，不是论文质量差。** 不能将其与全文精读评分简单加总排序。

| 候选 | 六维分数 | 本轮处置与可核验理由 |
|---|---|---|
| Reallocating Attention，CVPR | 4/3/2/3/2/4 | 已有队列→收录；补足推理模型head输出比较与理论/实现审计，完整正文及补充支撑 |
| [Beyond the Global Scores](https://arxiv.org/abs/2604.04863)，CVPR | 5/3/1/1/1/4 | 原队列P1保留；局部ADS/CGC与全局mass的区别有价值，尚未完成camera-ready/补充/代码一致性闸门 |
| [LEAD / Thinking in Uncertainty](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Thinking_in_Uncertainty_Mitigating_Hallucinations_in_MLRMs_with_Latent_Entropy-Aware_CVPR_2026_paper.html)，CVPR | 4/4/1/1/1/4 | **新增P1**；官方摘要提出熵门控连续embedding与视觉anchor，需拆分两组件并审计KV/输出预算 |
| [MIOH](https://openaccess.thecvf.com/content/CVPR2026/html/Min_Fine-Grained_Multi_Image_Object_Hallucination_Benchmark_CVPR_2026_paper.html)，CVPR | 4/4/1/1/1/4 | **新增P2**；多图存在/计数/属性/位置，需核对构造、模型版本、评测器与许可 |
| [Detection In-Depth Analysis](https://neurips.cc/virtual/2026/poster/139199)，NeurIPS官方题名页 | 5/4/1/1/1/5 | **新增P1**；摘要称token位置朴素基线可竞争，优先审计混淆与跨模型协议 |
| [VerDA / Complementary Visual Units](https://neurips.cc/virtual/2026/poster/149428)，同上 | 5/3/1/1/1/4 | **新增P1**；逐头visual cues与文本距离联合操作，需要同数随机、总量守恒及长度对照 |
| [Focus Matters](https://neurips.cc/virtual/2026/poster/155092)，同上 | 5/4/1/1/1/5 | **新增P1**；摘要区分视觉编码器attention与value贡献，待核对phase选择及mean-value干预 |
| [HALMES](https://neurips.cc/virtual/2026/poster/153080)，同上 | 5/3/1/1/1/4 | **新增P1**；选择性触发对比解码，需报告触发率、误伤、保召回和同预算对照 |
| [Correction Space Steering](https://neurips.cc/virtual/2026/poster/150994)，同上 | 5/3/1/1/1/4 | **新增P2**；低维空间+在线坐标预测，需审计训练依赖、秩假设与未知错误外推 |
| [VGDPO](https://neurips.cc/virtual/2026/poster/154431)，同上 | 5/3/1/1/1/4 | **新增P2**；squeezing与视觉依赖重权，需区分训练动力学观察、因果解释及监督成本 |
| [CORAL](https://neurips.cc/virtual/2026/poster/150874) / [OpenReview入口](https://openreview.net/forum?id=ek5KY0D3CL) | 5/4/1/1/1/5 | 原候选更新官方入口；评审有浏览器验证，不绕过；定理的对称性/依赖/随机阈值条件未精读，不声称已实现无条件FDR控制 |
| [Dual-Pathway](../papers/dual-pathway-circuits.md) | 不重复打分 | 与既有Note重复；arXiv v2于10-07上线并链接代码，仅加版本警告，保留v1正文与added_at |

新增优先候选共8篇（CVPR2、NeurIPS6）；1篇既有候选转精读，1篇既有Note加版本提醒，CORAL更新来源入口。其他题名命中留在扫描记录，不全部塞入主要阅读路径。已读摘要但未全文的候选不支持具体数值引用或机制定论。排除普通产品消息、泛LLM无直接迁移价值以及将hallucination指代特征补全的工作；未把有关键词的论文一概当作VLM幻觉研究。

## 4. 扫描范围、去重与证据缺口

NeurIPS公开快照含9,245个去重event链接（**包括tutorial/workshop等，不能称9,245篇主会论文**），`hallucin`题名命中56，55个页面解析到摘要；按VLM/visual/multimodal题名保留20条进行相关性审查。正文没有穷尽，标题不含关键词的相关工作也可能漏检。公开快照抓取时间2026-10-16 UTC，官方Downloads于10-17复查仍可检索关键题名；event页本轮直连受限，不能把缓存解析计数冒充实时全站统计。原始题名、官方URL、OpenReview入口及处置保存在[扫描记录](research-atlas-scan-20261017.json)。

去重使用标准化标题、稳定slug、paper_url与正文arXiv/DOI别名，而非只看front matter是否有独立ID。基线43篇均为automated；object40、attribute12、relation7（可多标签），主方向head16、logit10、representation10、training4、evaluation2、long-form1。外部依赖、benchmark、evidence type、baseline suitability尚无统一机器字段；本轮新Note已增加字段，但不将旧Note缺字段当作“无外部依赖/无实验证据”。

Dual-Pathway官方arXiv页面已确认v2和[作者代码](https://github.com/jiaxin26/DualPath-VLM)入口。新版本尚未完整复核，故**未改arxiv_version为v2，也未把venue升级为已复核NeurIPS**；优先下一轮做版本差异和decision核查。所有既有added_at保持不变。

## 5. 分类与组件

本轮方法可由已有head/path族表达，没有3篇已充分核验的新方法族证据；也未举证5篇同类歧义已显著阻碍发现。月份内已有10-03结构审计，本轮仅增加1篇、未增长10篇，也无新论文无法被当前导航发现的证据。故不迁移taxonomy、不新增UI组件或依赖。只同步首页、索引、方法目录、方向、CVPR比较矩阵与研究版图；未经精读的NeurIPS工作不进入机制关系图。

## 6. 交付与恢复

质量闸门：索引生成、Deep Note校验、公开边界检查、严格MkDocs构建、HTML本地链接及`git diff --check`。PR合并与Pages状态由GitHub实际结果解析，未发布前不推进成功checkpoint。本报告与扫描文件中的proposed cutoff只有在PR合并、部署及公开页面核验后才生效；恢复时先查同名分支/PR及合并commit，禁止重复收录。

仍待人工或后续核验：Reallocating官方实现、query轴与独立调参协议；新候选正文/补充/代码和公开评审；完整CCF目录覆盖；TPAMI/AI/IJCV本周逐文日期。以上缺口不是全轮阻断，也不是“无新论文”的证据。

---
title: 2026-11-21：MIOH 多图评测与 CVPR 补齐
description: 三届 CVPR 主会题名筛选、MIOH 证据审计与公开增量核验
tags: [Literature audit, CVPR, Evaluation, Multi-image]
---

# 2026-11-21 来源核验

从 [PR #18](https://github.com/ChenXi4232/vlm-hallucination-notes/pull/18) 合并后的 main 开始。上一轮 [Pages 部署](https://github.com/ChenXi4232/vlm-hallucination-notes/actions/runs/44458838066) 成功，LEAD 公开页实测可读，增量从 2026-11-19 边界日重查去重。CVPR 历史补齐另行计算。覆盖范围、日期口径和候选处置见 [扫描记录](https://github.com/ChenXi4232/vlm-hallucination-notes/blob/main/docs/reading-notes/research-atlas-scan-20261121.json)。

## CVPR 收录

[MIOH](../papers/mioh.md) 从原队列升为唯一新增精读。核对 CVF 主会论文、独立补充与 arXiv:2608.30653 v1，并对照 PDF 上的 Table 2 与 Figure 5。Figure 5 的 Qwen2-VL-7B 同一批图联合答题 80.0%，逐图问答再汇总 94.0%，限存在性。Table 2 的整体存在任务 Easy 62.4%，NI 30.0%。两项结果的样本和比较口径分别登记。

最需要控制的因素是联合/逐图提示、选项基率、每图有效分辨率、视觉 token 和调用次数。可以先分开对象识别与图号归属，再测关系与计数。Table 2 的 HN 计数高于 Easy 5.2 个百分点，原文的地板效应解释还需逐题随机基线与配对数据。补充 Figure V 记录对象错认与关系错判两类实例。完整样本、代码和派生许可待核。未找到公开评审页面，所列问题是本站审计。

## 官方论文集与政策

第七版 [CCF 发布页](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml) 的[勘误后 PDF](https://www.ccf.org.cn/ccf/contentcore/resource/download?ID=112CF3BF7E1140ACEB271ADAED12A67ADFABB8FF099E40C2759502A85C8A281F) 已重新核对。人工智能 A 类相关会议为 AAAI、NeurIPS、ACL、CVPR、ICCV、ICML、ICLR，期刊为 Artificial Intelligence、TPAMI、IJCV、JMLR。图形学与多媒体分册另列 ACM MM 为 A 类。相关的 EMNLP、ECCV、IJCAI 为 B 类。网页分类和修订 PDF 在 ICLR、IJCAI 有差异，以正式修订版为准。Findings、Workshop 与主会分别登记。

| 来源 | 2026-11-21 状态及覆盖 |
|---|---|
| [CVF 发布目录](https://openaccess.thecvf.com/menu) | CVPR 2026 主会 05-23、Workshop 05-26、Findings 05-27（出版方明示的日期）。联系 [会议日历](https://cvpr.thecvf.com/Conferences/2026/Dates) 可区分 02-20 录用通知、06-05 至 06-07 主会和论文集上线。本轮跑主会三届题名过滤，未重扫非主会轨道。 |
| [CVPR 2027 Dates](https://cvpr.thecvf.com/Conferences/2027/Dates) | 主会注册/摘要、全文、补充分别为 2026-11-10、11-16、11-23 AoE，录用决定 2027-02-25 AoE。正式论文集待公开。官方 Dates 现列主会 sessions 为 2027-06-22 至 06-24，替代上一轮笔记转录的 06-22 至 06-25。 |
| [NeurIPS 2026 Downloads](https://neurips.cc/Downloads/2026) / [Proceedings](https://proceedings.neurips.cc/) | 已有 2026 官方会议论文页，下载索引 9,276 个去重活动入口，含非论文活动，与 11-19 快照数量相同。正式论文集索引仍至 2025，未见 2026 卷。本轮未逐条比较同数量下的事件替换。 |
| [ICML 2026 PMLR 306](https://proceedings.mlr.press/v306/) | 正式发布时间 2026-09-29。沿用 6,552 题名、19 篇直接相关摘要的历史游标。 |
| [ACL 2026](https://aclanthology.org/events/acl-2026/) / [EMNLP 2026 主会](https://aclanthology.org/volumes/2026.emnlp-main/) / [Findings](https://aclanthology.org/volumes/2026.findings-emnlp/) | 正式卷可查。EMNLP 分卷去掉卷首分别为 2,704 / 2,478，末尾 ID 同为 .2704 / .2478，未见编号扩张。没有逐项复查同 ID 版本，未触发整卷重扫。 |
| [ICLR 2026 论文](https://iclr.cc/virtual/2026/papers.html) / [ICLR 2027 日历](https://iclr.cc/Conferences/2027/Dates) / [OpenReview](https://openreview.net/group?id=ICLR.cc/2027/Conference) | 2026 论文入口仍可访问，2027 已进入审稿讨论阶段。未确认 2027 正式录用批次。 |
| [AAAI 2026](https://aaai.org/proceeding/aaai-40-2026/) / [AAAI 2027](https://aaai.org/conference/aaai/aaai-27/submission-instructions/) | 前者已有分期论文集。2027 主技术轨最终录用通知定于 2026-11-30 AoE，未见正式批次。 |
| [ICCV 2025](https://openaccess.thecvf.com/ICCV2025) / [ICCV 2027](https://iccv.thecvf.com/Conferences/2027) | 已有 CVF 2025 索引，2027 官网为会议信息。未见 2027 正式论文页。 |
| [IJCAI 2026](https://ijcai.org/proceedings/2026/) / [ECCV 2026](https://eccv.ecva.net/Conferences/2026) | 以前已公开的正式目录。IJCAI 首发日待核。ECCV 沿用旧记录的 2026-09-09 Springer 主会各卷公告。 |
| [ACM MM 2026](https://doi.org/10.1145/3767308) | Crossref 出版方记录复核为 11-09 在线、11-10 纸本。沿用前次 1,857 个同卷 DOI 的题名游标，完整摘要与覆盖待续。 |
| [IJCV 论文页](https://link.springer.com/article/10.1007/s11263-026-03118-1) / [JMLR 卷 27](https://jmlr.org/papers/v27/) / [TPAMI Early Access](https://www.computer.org/csdl/journal/tp/early-access) / [Artificial Intelligence 在版论文](https://www.sciencedirect.com/journal/artificial-intelligence/articles-in-press) | IJCV 有 11-10 出版的相邻分割论文，本轮补查。JMLR 卷可读，TPAMI 入口未验证完整逐条列表，AI 在版入口返回 403。期刊逐篇游标未推进。 |

[CVPR 2027 作者指南](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines) 与 [审稿指南](https://cvpr.thecvf.com/Conferences/2027/ReviewerGuidelines) 均重查。匿名 LLM Usage Statement、互惠审稿资格，以及同期工作引用和合理可行的比较规则，未识别到相对 11-19 核验的变化。官方 [CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers) 对会前公开论文仅给出计划，实际首发日待核。

## 新候选与取舍

三届 CVF 主会输入为 4,042（2026）、2,871（2025）、2,716（2024）条。固定题名关键词筛得 42、19、10 项，涵盖 hallucin、visual faithfulness、visual counterfact、visual grounding/evidence in、spatial reasoning gap、VisRes Bench。题名命中数含已有、非目标领域或尚需复筛的条目。新正式卷批次未识别，三届结果用于已有历史补齐。摘要复查集中在下表优先项，未穷尽非关键词论文。11-19 边界日起的 arXiv 检索使用视觉/多模态幻觉、grounding、visual evidence，并去重已有 Note 与候选。IJCV 单篇为前轮窗口内漏项回查。

六项分数按直接相关性、新颖性、机制证据、实验完整性、可复现与低算力、知识库增量排列。摘要候选低分表示可核对证据深度有限。

| 记录 | 六项分数 | 处置 |
|---|---|---|
| [MIOH](../papers/mioh.md) · CVPR 2026 主会 | 5/4/3/4/2/5 | 旧候选升为精读，增加跨图诊断，对应模型可复核程度见 Note。 |
| [OSI-Bench](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_From_Indoor_to_Open_World_Revealing_the_Spatial_Reasoning_Gap_CVPR_2026_paper.html) · CVPR 2026 主会 · arXiv:2512.19683 | 4/4/2/2/3/5 | 新 P1。室外 3D 度量真值和 blinding 可补空间关系设计，需核对异常场景、传感器真值和公开包。 |
| [VisRes Bench](https://openaccess.thecvf.com/content/CVPR2026/html/Tortei_VisRes_Bench_On_Evaluating_the_Visual_Reasoning_Capabilities_of_VLMs_CVPR_2026_paper.html) · CVPR 2026 主会 | 3/4/1/2/1/4 | 新 P2。可测试视觉规律的强制依赖，全文、许可和与对象幻觉的外推边界待核。 |
| [Contrast Where It Matters](https://arxiv.org/abs/2611.25524v1) · 2026-11-19 提交 · 预印本 | 5/3/1/2/2/4 | 新 P1。证据引导的对比解码，优先查局部视觉证据选择、同预算对照、召回与相邻对比方法的区别。 |
| [When Safety Rationales Hallucinate](https://arxiv.org/abs/2611.25793v1) · 2026-11-19 提交 · 预印本 | 2/3/1/2/1/3 | 本轮不入队。视觉区域及属性关系证据有迁移价值，任务主体为安全理由与策略归因，需靠单独实验验证开放对象评测的价值。 |
| [Robust Reasoning Segmentation](https://doi.org/10.1007/s11263-026-03118-1) · IJCV · 2026-11-10 出版 | 2/3/1/2/2/2 | 本轮不入队。研究中心为推理分割和能力保持，未从出版页确认与幻觉机制直接对应的对照。 |

Beyond the Global Scores 继续保留 [11-19 复现审计](research-atlas-20261119.md#beyond-the-global-scores) 中的模型与解码口径差异。旧候选 FINER、Envision 与 HalLoc 保留原游标。本轮未发现达到精读门槛的新增严格理论论文。

## 覆盖与站点变更

基础 front matter 覆盖 46 篇，按主方向分别为 Head/Path 17、Token/Logit 12、Representation/Activation 10、Training/Alignment 4、Evaluation/Benchmark 2、Long-form 1。对象、属性、关系分别有 42、12、7 篇显式标签，允许重合。16 篇标作 CVPR，1 篇标作 CVPR Findings。无参数更新与离线校准用不同字段值登记。外部依赖、证据类型和 baseline suitability 仅各有 2 篇使用对应独立字段，benchmark 多靠标签和正文，研究关系以已有矩阵的来源类型为准。这些字段的缺口限制跨库机器统计。

收录后共 47 篇，保持原 46 篇的 added_at。本轮只维护已有索引、评测入口、方法目录、方向、研究版图和 CVPR 矩阵。已有 Evaluation / Benchmark 可表达 MIOH，未证实新稳定方法族或妨碍检索的同类标签歧义。相对上一轮只增加 1 篇，现有入口能直接发现新 Note，组件改版缺乏依据。本轮未运行复现实验。

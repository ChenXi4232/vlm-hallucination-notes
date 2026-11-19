---
title: 2026-11-19：CVPR 精读、EMNLP 批次与复现审计
description: CVPR 论文证据、EMNLP 正式卷扫描与历史复现核验
tags: [Literature audit, CVPR, EMNLP, NeurIPS]
---

# 2026-11-19 来源核验

从已部署的[上轮记录](research-atlas-20261017.md)继续。基线为主分支 44 篇 Deep Paper Notes、PR [#17](https://github.com/ChenXi4232/vlm-hallucination-notes/pull/17) 与[成功的 Pages 构建](https://github.com/ChenXi4232/vlm-hallucination-notes/actions/runs/38992730583)。本轮核查窗口为 2026-10-18 至 2026-11-19，另继续 CVPR 历史补齐。候选评审、代码检查与文献证据均为自动化分析；实验建议尚未运行。

## 1. 新增精读与历史审计补交

| 论文 | 可追溯证据 | 复现边界 |
|---|---|---|
| [LEAD](../papers/lead-entropy-aware-decoding.md) · CVPR 2026 主会 | R1-Onevision 的 MMHalu 3.52→3.80，Bingo 3.65→3.84，POPE adversarial 82.5→83.9%（Table 2） | 论文的三种视觉特殊词嵌入均值与公开实现的图像 pad 锚点不同。正文与补充的 InternVL 型号不一致，未引用该组数字；主结果采用表中 R1-Onevision 对照。 |
| [VisER](../papers/viser.md) · EMNLP 2026 主会 | COCO 四模型平均 AUROC 由最佳单一对照 81.26 升至 84.89（Table 1）；LLaVA-1.5-7B 对照原图、置空、打乱 patch 的 AUROC 为 86.17、71.38、77.99（Table 5） | 官方仓库目前仅有占位文件。指标 grounded 为正类，prefix 相似度是代理；后验对象级检测的结果不能直接外推为生成时因果贡献。 |

[Dual-Pathway](../papers/dual-pathway-circuits.md) 更新原 Note 至 arXiv v2，核对官方会议 Poster 和作者代码并保留首次收录日。发布脚本默认发现与干预评估索引范围重叠；此结论限于发布代码的默认路径，论文实际运行的样本 ID 仍待确认。

### Beyond the Global Scores 暂缓收录

已复核 [CVF 正文与补充](https://openaccess.thecvf.com/content/CVPR2026/html/Nguyen_Beyond_the_Global_Scores_Fine-Grained_Token_Grounding_as_a_Robust_CVPR_2026_paper.html)、[arXiv v1](https://arxiv.org/abs/2604.04863v1) 和[作者代码的固定提交](https://github.com/tuandung2812alt3/token-grounding-detector/tree/30257083e326e763938e96de6d9cbc717937a5eb)。恢复 10 月 17 日工作稿中的核验，按待澄清的复现项登记。

| 核验项 | 公开证据与待确认问题 |
|---|---|
| Qwen 骨干 | 补充 Table 7 为 Qwen2.5-VL-8B，正文 Table 2 与发布配置为 7B。复现前应确认实际 checkpoint。 |
| 解码协议 | 补充 §6.1 有 `top-p=20`、`top-p=50`，超出标准 nucleus probability 的取值范围；§6.2 的 MetaToken 适配描述为 greedy。需澄清参数含义和各自适用表格。 |
| 代码链 | `features/extractor.py` 和 `scripts/train_and_eval.py` 引用的 `features/attention.py`、`analysis/ablation.py`、`scripts/eval_baselines.py` 未出现在固定提交的完整文件树中。此为静态核查；实际运行状态待验证。 |
| ADS | `features/ads.py` 在计算 blob mass 前做最小值平移与视觉范围归一化。复现应单独标记公式版与提交中的实现版。 |
| 指标 | LLaVA 的 Table 2 XGB AUC 为 0.88，Table 4 的 ADS+CGC 为 0.92。分别按各表协议引用；POPE 幻觉类 F1 0.41、AUC 0.75（Table 3）。低空间熵仍可能来自对错误区域的集中关注。 |

## 2. 正式论文集与投稿政策

以[CCF 第七版发布页](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)附[勘误后目录 PDF](https://www.ccf.org.cn/ccf/contentcore/resource/download?ID=112CF3BF7E1140ACEB271ADAED12A67ADFABB8FF099E40C2759502A85C8A281F)为准。第 57–58 页中 CVPR、ICCV、AAAI、NeurIPS、ICML、ACL、ICLR 为 A 类，EMNLP、ECCV、IJCAI 为 B 类。分类网页和 PDF 对 ICLR、IJCAI 的信息存在版本差异。第 47 页列 ACM MM 为图形学与多媒体 A 类；第 51 页列 AI、TPAMI、IJCV、JMLR 为人工智能 A 类期刊。正式长文、Findings 和 Workshop 分轨，期刊按在线优先与卷期分别核验。

| 来源 | 2026-11-19 核验与处理 |
|---|---|
| [CVPR 2026 主会](https://openaccess.thecvf.com/CVPR2026?day=all) | 正式论文页继续可检索。本轮快照有 4,042 个去重主会入口，题名含 `hallucin` 39 项，含跨领域结果；另对优先候选核对正文和补充。全卷真实公开日沿用旧账本口径，未取得新的原始公告。 |
| [EMNLP 2026 主会](https://aclanthology.org/volumes/2026.emnlp-main/)与 [Findings](https://aclanthology.org/volumes/2026.findings-emnlp/) | 正式卷可查，Anthology 书目信息为 2026 年 10 月。[出版方](https://github.com/acl-org/acl-anthology/pull/10522)在 10 月 24 日导入卷元数据，对应[生产站发布](https://github.com/acl-org/acl-anthology/actions/runs/40070330778)同日成功。确切的页面传播时间未知，本账本在 11 月 19 日实测页面可读。会议为 10 月 24–29 日。本轮触发正式卷批次扫描。 |
| [NeurIPS 2026 Downloads](https://neurips.cc/Downloads/2026)与[正式论文集](https://papers.nips.cc/) | 2026 官方会议论文页继续可查，正式论文集索引仍至 2025。对旧候选复核版本，保留 10 月题名快照的覆盖边界。本轮快照 9,276 个去重事件入口，含教程和 Workshop；56 个 `hallucin` 题名命中中，21 个含视觉术语。会议页首次确认仍为 10 月 17 日，准确公开日未知。 |
| [ICML PMLR 306](https://proceedings.mlr.press/v306/) | 正式卷仍标 2026-09-29。沿用已完成的 6,552 项标题扫描、19 篇相关摘要审查。 |
| [ACL 2026](https://aclanthology.org/events/acl-2026/) | 正式卷已见于 10 月账本，本轮未识别需要重扫的新发行批次。 |
| [AAAI 2026](https://aaai.org/proceeding/aaai-40-2026/) 与 [ICCV 2025](https://openaccess.thecvf.com/ICCV2025) | 既有正式索引。AAAI 分期刊载，单期日期与整套上线日分别记录。 |
| [ECCV 2026](https://eccv.ecva.net/Conferences/2026) | 会议官网 9 月 9 日公告列出 Springer 主会正式卷 I–LXXVIII，早于本轮增量窗。 |
| [ICLR 2026](https://iclr.cc/virtual/2026/papers.html) 与 [ICLR 2027](https://www.iclr.cc/Conferences/2027/Dates) | 2026 论文目录链接到正式 OpenReview 记录；2027 已进入作者与审稿人讨论阶段，尚未核验到 2027 正式论文批次。 |
| [IJCAI 2026](https://ijcai.org/proceedings/2026/) | 正式卷和单篇页面可查，首发日仍待核。 |
| [ACM MM 2026](https://doi.org/10.1145/3767308) | [出版方 DOI 记录](https://api.crossref.org/works/10.1145/3767308)标注 11 月 9 日在线出版，纸本为 11 月 10 日，会议为 11 月 10–14 日。ACM DL 直连为 403；Crossref 三页按卷名与 DOI 前缀保留 1,857 个去重题名，其中 20 项含 `hallucin`。元数据未提供摘要，后续须补摘要与卷覆盖核对。 |
| [AAAI 2027](https://aaai.org/conference/aaai/aaai-27/) | 主会录用通知在 11 月 30 日 AoE，属未来事项；未查到正式批次。 |
| [JMLR 27](https://jmlr.org/papers/v27/)、[IJCV 在线优先](https://link.springer.com/journal/11263/online-first)、[TPAMI Early Access](https://www.computer.org/csdl/journal/tp/early-access)、[Artificial Intelligence 在版论文](https://www.sciencedirect.com/journal/artificial-intelligence/articles-in-press) | JMLR 卷可访问；IJCV 返回陈旧条目，TPAMI 与 Artificial Intelligence 存在访问缺口。逐文上线审计未完成，覆盖游标暂不推进。 |

[CVPR 2027 Author Guidelines](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines) 与 [Reviewer Guidelines](https://cvpr.thecvf.com/Conferences/2027/ReviewerGuidelines) 已公开。投稿须在正文后、参考文献前附匿名 **LLM Usage Statement**，列明所用工具、影响部分与使用程度，文字编辑也在披露范围内；未使用须明确声明。该声明不计入正文 8 页，缺失会触发 desk rejection。审稿可选用官方 OpenReview 助手，评分和建议仍由审稿人填写。官方按 2026-09-15 起的 contemporaneous work 规则处理同期论文，仍要求引用讨论，并在合理可行时作实证比较；影响过投稿的相关工作仍须按 prior work 引用。作者互惠审稿资格与例外见指南。

[Dates](https://cvpr.thecvf.com/Conferences/2027/Dates) 与 [CFP](https://cvpr.thecvf.com/Conferences/2027/CallForPapers) 的注册、全文和补充日期仍为 11 月 10 日、16 日、23 日（AoE）。补充截止 11 月 23 日 23:59 AoE，即北京时间 11 月 24 日 19:59。CVPR 2027 录用决定定于 2027 年 2 月 25 日，主会为 6 月 22–25 日；官方的论文集公开计划属于未来安排。

## 3. 候选与版本处理

EMNLP 批次从两个正式卷提取论文 ID、题名及内嵌摘要，移除 `.0` 卷首。以 `hallucin`、`grounding/grounded`、`faithful`、`misground`、`visual evidence/reliance/prior` 及 `perceptual/visual error/failure/bias` 筛题名，再检查摘要或题名含视觉/多模态术语及 `hallucin`。覆盖为关键词扫描；无相关术语的工作仍可能漏检。其他 EMNLP 轨道未全扫。

| 卷 | 题名及摘要 | 题名初筛 | 加视觉词 | 加 `hallucin` |
|---|---:|---:|---:|---:|
| Main | 2,704 | 164 | 87 | 26 |
| Findings | 2,478 | 154 | 67 | 20 |

六项分数按直接相关性、新颖性、机制证据、实验完整性、可复现与低算力、知识库增量排列。摘要初筛中的低证据分反映核验深度；不得把它解读为论文质量结论。

| 候选 | 六项分数 | 处置和下一步 |
|---|---|---|
| [LEAD](../papers/lead-entropy-aware-decoding.md) · CVPR | 4/4/2/3/3/5 | 旧队列升为精读。已核对正文、补充与代码，保留实验口径缺口。 |
| [VisER](../papers/viser.md) · EMNLP | 5/4/3/4/2/5 | 旧队列升为精读。方法可与 real/null 研究直接比较，标注代码当前缺口。 |
| [Beyond the Global Scores](https://arxiv.org/abs/2604.04863v1)（CVPR 主会） | 5/3/2/3/1/4 | P1 暂缓，保留补充、正文和实现的冲突记录。 |
| [PAVE](https://neurips.cc/virtual/2026/poster/150489)（NeurIPS 官方会议页） | 4/3/1/1/1/4 | 恢复旧稿的 P2 分级。逐图 prefill basis 与离线子空间，后续核对固定基底、校准划分和等预算 Recall。 |
| [FlashAttention with Statistics](https://arxiv.org/abs/2610.21483)（预印本） | 3/4/2/2/2/4 | 恢复旧稿的跨方向候选，限于注意统计提取效率。H100/Qwen3-8B 环境中的成本随长度变化，向 VLM 空间统计迁移需要独立测量。 |
| [Focus Matters](https://arxiv.org/abs/2604.03556v2)（NeurIPS 官方会议页、arXiv v2） | 5/4/2/2/3/5 | 原 P1；v2 为 11 月 7 日，优先查视觉编码器的值分支、随机替换对照、相同图像均值及选层迁移。 |
| [HALMES](https://arxiv.org/abs/2611.09957v1)（NeurIPS 官方会议页、arXiv v1） | 5/4/1/1/2/4 | 原 P1，补公开预印本；优先审计 attention 前驱信号的因果时点、对比解码触发预算和真对象保留率。 |
| [OmniHallu](https://aclanthology.org/2026.findings-emnlp.644/)（EMNLP Findings） | 4/3/1/1/2/4 | 以 Anthology PDF 和 arXiv 元数据镜像核对作者与摘要，补正式标题和链接。跨模态 claim 标注、生成与理解的评估协议待精读。 |
| [Say Less, Hallucinate Less?](https://arxiv.org/abs/2611.23179)（预印本，11 月 17 日） | 5/3/2/2/3/4 | 新候选。检查早 EOS 对照、相同覆盖率下的幻觉率、解码和偏好训练共同作用。 |
| [Where Hallucinations Live](https://aclanthology.org/2026.emnlp-main.2005/)（主会） | 5/4/1/1/1/5 | 新 P1。优先核对跨架构 VQ circuit 的定义、二分类与开放生成证据和组件对照。 |
| [BRACS](https://aclanthology.org/2026.emnlp-main.1662/)（主会） | 5/4/1/1/1/5 | 新 P1。grounding barrier 门控的闭式残差校正，需比较同触发率与同强度下的 Recall 和延迟。 |
| [Global-to-Local Visual Attention Correction](https://aclanthology.org/2026.emnlp-main.2272/)（主会） | 5/3/1/1/1/4 | 新 P1。核对尾部新增幻觉与位置和长度的混淆，及局部选择对 Recall 的影响。 |
| [Target-Binding](https://aclanthology.org/2026.emnlp-main.691/)（主会） | 4/4/1/1/1/4 | 新 P2。多图中可见证据源归错的检测，核对位置控制、图像距离和源标签。 |
| [SAFE](https://aclanthology.org/2026.findings-emnlp.140/)（Findings） | 5/4/1/1/1/5 | 新 P1。查真实与视觉消融 logits 的同前缀比较及输入消融偏差，再核对解码收益。 |
| [OViP](https://aclanthology.org/2026.findings-emnlp.674/)（Findings） | 4/4/1/1/1/4 | 新 P2。当前模型幻觉生成 diffusion 负图供偏好训练，需查对象更改控制、Recall 和训练总预算。 |
| [Beyond Language Priors](https://doi.org/10.1145/3767308.3836058)（ACM MM） | 5/4/1/1/1/5 | 新 P1。正式 DOI、[会议议程](https://2026.acmmm.org/site/ACMMM2026_Full_Programme.pdf)与[预印本](https://arxiv.org/abs/2609.00231)交叉核对；优先查视觉来源与语言先验混淆，及对象缺失和被误读的控制。 |
| [Beyond the Logits / LAVIG](https://doi.org/10.1145/3767308.3835945)（ACM MM） | 4/3/1/1/1/4 | 新 P2。有正式 DOI 和[官方议程摘要](https://2026.acmmm.org/site/technical-programme.html)；核对层级选择、可比预算和输出覆盖。 |

本轮 9 条新入队，2 篇既有候选转精读，另补交旧稿的 2 条候选分级和 1 段复现审计。候选池筛除仅同名的图像生成伪影与无明确 VLM grounding 关联的文本工作。用正式 ID、DOI/arXiv、归一标题与作者集合匹配旧队列；同一工作换版本不另计。

## 4. 分类、交付和恢复

沿用已有分类方法与阅读路径。本轮候选可映射到视觉证据诊断、检测或解码干预。新增论文关系仅表示实际共享的研究问题或比较基线。基线有 44 篇，全部为 `automated`；主要方向分布为 Head 17、Token 10、Representation 10、Training 4、Evaluation 2、Long-form 1。两篇新增均归到原 Token / Logit 方向；现有条目的证据类型、外部依赖及 baseline 字段覆盖不全，缺字段只能记为未登记。既有分类与组件足以覆盖新增内容。

[扫描记录](research-atlas-scan-20261119.json)保存来源状态、候选处置、覆盖边界和截止点。只有对应 PR 合并、Pages 构建成功并核验公开页面后，拟定截止点才生效。期刊逐文核验及未完成的论文集候选保留各自覆盖游标。按最新 `main` 的 PR 与部署记录检查交付，避免重复提交历史成果。

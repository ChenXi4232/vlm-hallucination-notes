---
title: "THRONE: An Object-based Hallucination Benchmark for the Free-form Generations of Large Vision-Language Models"
description: 面向自由生成的对象级幻觉基准，以开放语言模型抽取对象陈述并用类别平衡指标评价
authors: [Prannay Kaul, Zhizhong Li, Hao Yang, Yonatan Dukler, Ashwin Swaminathan, C. J. Taylor, Stefano Soatto]
venue: CVPR
year: 2024
resource_type: Benchmark 论文
direction: Evaluation / Benchmark
hallucination_type: [Object hallucination, Free-form generation]
method_level: [Evaluation-level]
training: No training
status: 已精读
source_status: CVPR 2024 官方论文与补充材料已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_THRONE_An_Object-based_Hallucination_Benchmark_for_the_Free-form_Generations_of_CVPR_2024_paper.html
overview_figure: ../assets/images/papers/throne-overview.png
overview_figure_source: Figure 1 from the official CVPR 2024 paper
tags: [THRONE, Benchmark, Free-form generation, Object hallucination, CHAIR]
---

# THRONE

<div class="paper-meta"><span>CVPR 2024</span><span>Evaluation / Benchmark</span><span>已精读</span></div>

[论文原文](https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_THRONE_An_Object-based_Hallucination_Benchmark_for_the_Free-form_Generations_of_CVPR_2024_paper.html){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>THRONE 不再用“图里有没有某对象”的封闭式提问替代真实生成，而是先让 LVLM 自由描述，再由多个开放语言模型把描述转成逐对象真值判断，最后以类别平衡的精确率、召回率和 F 分数衡量 object hallucination。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/throne-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/throne-overview.png" alt="THRONE 官方评测流程"></a><figcaption>官方方法概览图（论文 Figure 1）：自由生成、对象类别问题化、多个语言模型回答与投票汇总。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 核心问题 | polling-based yes/no 结果能否代表自由描述中的对象幻觉 |
| 方法 | 中性提示生成描述；按 80 个 COCO 类别构造抽取式问题；多个开放 LLM 独立判断并一致投票 |
| 数据 | COCO 2017 validation 5,000 图像，约 40 万次类别问答/评估模型 |
| 指标 | overall 与 class-balanced precision、recall、$F_{0.5}$；优先惩罚虚构对象 |
| 价值 | 将“会否被提示诱导说 yes”与“是否会主动生成不存在对象”分开 |

## 2. 研究背景

对象幻觉常由 POPE 等二元问答或 CHAIR 等词表匹配测量。前者改变了生成任务本身，后者对同义词、复合名词和长描述的处理较脆弱。THRONE 把目标明确为 Type-I：模型在没有对象暗示的自由生成里主动陈述了不存在的对象。论文进一步展示 Type-I 与 Type-II polling 排名并不稳定一致，因此二元准确率不能直接替代开放生成可靠性。

它的关键取舍是引入外部 LLM 作为语义解析器。相比字符串匹配，这能理解“没有人”“一对滑雪板”等自然表达；代价是评价器偏差、版本漂移和调用成本。为降低单个评价器偶然错误，作者使用多模型一致投票，并将分歧样本标为忽略，而不是强制多数表决。

## 3. 方法详解

对每张图使用不含目标类别的中性 prompt 获得一段描述。随后针对 COCO 80 类逐一形成“这段文字是否声称存在 X”式抽取任务，FLAN-T5 系列评价器只看文本回答。将其与 COCO 标注中的对象集合对齐即可得到 TP、FP、FN。论文同时给出 micro 聚合和先按类计算再平均的 macro 指标；后者避免 person、car 等高频类别支配结论。

选择 $F_{0.5}$ 表明 precision 权重高于 recall，适合把错误陈述看得比漏述更严重的可靠性场景，但也可能奖励极度简短的描述。因此阅读结果时必须同时检查 recall，并记录输出长度。评价器一致投票提高 precision，却会把困难表达排除出统计，实际报告应附带 ignore 比例。

## 4. 实验设计

### 4.1 设置

覆盖当时多种开源 LVLM，在同一 COCO 2017 validation 集上自由生成。每个描述对 80 类运行 abstractive QA；主指标为 $P_{CLS}$、$R_{CLS}$、$F_{CLS}^{0.5}$，并报告 overall 版本、CHAIR 和 POPE 作为外部参照。评估成本随图片数、类别数和评价器数线性增长。

### 4.2 主结果

| 模型 / 指标 | Precision | Recall | $F_{0.5}$ | 来源 |
|---|---:|---:|---:|---|
| LLaVA-v1.5-7B，overall | 68.1 | 61.0 | 64.4 | Table 1 |
| LLaVA-v1.5-7B，class-balanced | 69.9 | 56.4 | 62.5 | Table 1 |
| LLaVA-Mistral，class-balanced | — | — | 70.8 | Table 1 |

结果说明 macro 与 micro 口径会改变模型观感；高频类别上表现好并不意味着长尾对象可靠。论文报告的一个关键观察是 THRONE 排名与 polling-based benchmark 并非单调一致，支持将二者作为互补终点而非相互替代。

### 4.3 消融与分析实验

作者比较不同评价 LLM、投票规则和传统指标。多评价器一致票显著减少单模型误判，但覆盖率会下降；类别平衡后，一些总体 precision 较高的模型因长尾类别下降而被重新排序。与 CHAIR 的比较显示语义 QA 能处理词形和上下文否定，但仍受 COCO 预定义类别边界限制。论文还分析 Type-I/Type-II 相关性不足，构成其最有意义的 construct-validity 证据。

## 5. 亮点与贡献

- 明确分离自由生成幻觉与直接询问诱发的偏差。
- 以 class-balanced 指标控制对象频率，并保留 recall 作为“少说话”警戒线。
- 评价流程可迁移到同义表达，不依赖完全匹配。

## 6. 局限

固定 80 类无法覆盖开放世界；COCO annotation omission 会把真实对象误计为 hallucination；外部 LLM 的 prompt、模型版本和一致票策略都是隐藏超参。$F_{0.5}$ 体现应用偏好而非普适真理。论文没有用自然域外数据充分验证评价器迁移，也没有为所有模型报告多次采样置信区间。

## 7. 与我的研究关系

THRONE 适合作为自由生成主终点，并与对象删除反事实、POPE 和 token-level 证据指标组成分层评估。若一个干预只改善 polling、却不改善 THRONE，应优先怀疑任务形式或 answer prior；若 THRONE precision 上升但 recall/长度下降，则应怀疑保守生成而非证据利用增强。

## 8. 可执行的后续实验

1. 在同一解码设置下联合报告 THRONE、CHAIR、Recall、长度和 distinct-n。
2. 对删除目标、匹配 sham 和自然图三组分别运行，检查编辑伪迹是否影响评价器。
3. 对评价器分歧样本人工复核 100 条，并公开 error taxonomy 与 ignore rate。
4. 以 bootstrap 对图片重采样，给出模型差值的 95% CI。

## 9. 复现清单

- [x] 官方 Figure 1、主表与评价流程已登记
- [ ] 固定生成 prompt、max tokens 与 decoding seed
- [ ] 固定评价器 checkpoint、prompt 和投票规则
- [ ] 保存逐类 TP/FP/FN 和被忽略样本
- [ ] 同时报 macro/micro、recall 与长度

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 将自由生成作为独立构念 |
| 证据强度 | 4/5 | 大规模逐类评价和多评价器核对 |
| 可复现性 | 3/5 | 流程清楚，但外部 LLM 带版本依赖 |
| 相关性 | 5/5 | 直接约束开放生成终点 |

## 11. 来源边界

本文依据 CVPR 2024 官方论文与补充材料整理。数字来自原文 Table 1；对评价器偏差、编辑对照与分层终点的讨论属于本站分析，未声称已独立复跑。

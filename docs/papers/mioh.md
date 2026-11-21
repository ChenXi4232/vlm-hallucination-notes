---
title: "Fine-Grained Multi-Image Object Hallucination Benchmark"
description: 将跨图对象错误拆为存在、计数、属性和位置，并用同图逐张作答检查联合输入代价
authors: [Joonki Min, Chaeyun Kim, Hyungwook Choi, Yejin Kim, Kihyun Kim, Yohan Jo, Joonseok Lee]
venue: CVPR
year: 2026
resource_type: Benchmark 论文
direction: Evaluation / Benchmark
hallucination_type: [Object hallucination, Counting, Attribute hallucination, Relation hallucination]
method_level: [Evaluation-level]
training: No training
status: 已精读
source_status: CVPR 2026 主会，CVF 正文与独立补充已核对，arXiv v1 已交叉核验
review_state: automated
arxiv_version: v1
added_at: 2026-11-21
last_verified: 2026-11-21
paper_url: https://openaccess.thecvf.com/content/CVPR2026/html/Min_Fine-Grained_Multi_Image_Object_Hallucination_Benchmark_CVPR_2026_paper.html
overview_figure: null
overview_figure_source: CVF 正文 Figure 1 有官方概览，图内多来源图片的转载许可未核验，使用本站等价抽象
tags: [MIOH, Multi-image, Benchmark, Object hallucination, Counting, Attribute binding, Spatial relations, COCO-ReM, PACO, SVG, Counterfactual]
---

# Fine-Grained Multi-Image Object Hallucination Benchmark

<div class="paper-meta"><span>CVPR 2026 主会</span><span>Benchmark</span><span>Evaluation-level</span><span>No training</span></div>

[CVF 论文页](https://openaccess.thecvf.com/content/CVPR2026/html/Min_Fine-Grained_Multi_Image_Object_Hallucination_Benchmark_CVPR_2026_paper.html){ .kb-button .primary } [CVF 正文](https://openaccess.thecvf.com/content/CVPR2026/papers/Min_Fine-Grained_Multi_Image_Object_Hallucination_Benchmark_CVPR_2026_paper.pdf){ .kb-button } [独立补充](https://openaccess.thecvf.com/content/CVPR2026/supplemental/Min_Fine-Grained_Multi_Image_CVPR_2026_supplemental.pdf){ .kb-button } [arXiv v1](https://arxiv.org/abs/2608.30653v1){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>MIOH 把跨图对象问答拆成四类视觉任务和三类整合问题。存在性实验中，同批图像逐张作答再汇总优于一次联合输入。逐图作答同时改变了提示、调用次数和答案汇总方式，行为结果无法定位模型内部组件。</p></div>

## 官方方法概览图

<div class="paper-figure">CVF 正文 Figure 1 提供官方概览。图中各来源图片的转载许可尚未确认，本页用流程图展示本站等价抽象。</div>

~~~mermaid
flowchart TD
    A["对象、属性、关系标注"] --> B["按难度抽取图像"]
    B --> C["按任务与推理模式生成选项"]
    C --> D["三位标注者核对"]
    D --> E["模型回答与分层计分"]
~~~

上游通过规则、CLIP 或共现统计构造压力层，标注者核对题目与真值，随后比较选择题准确率。压力作用于评测输入。模型权重和推理内部组件保持原样。

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 研究对象 | 多图选择题中的对象存在性、计数、属性绑定、空间关系绑定 |
| 问题范围 | 综合（全图聚合）、比较（识别差异）、选择（找符合条件的图或证据） |
| 压力变量 | HP 难正例、HN 难负例、NI 图像数量、Easy 常规难度 |
| 方法类型与位置 | Evaluation-only，操控图像集合、题目与选项，无训练或内部干预 |
| 外部依赖 | 数据构造依赖 COCO-ReM、PACO、SVG 标注和 CLIP。三位标注者核对题目 |
| 最适合角色 | 多图评测协议和逐图聚合行为基线，有条件作为可复算 benchmark |

## 2. 研究背景与核心矛盾

一个样本由有序图像组、问题、候选答案和标注真值组成。误检与漏检、数量错算、属性绑定错误、空间关系或图号绑定错误都可能降低准确率，解析失败或弃答亦然。论文 §2 将其与主要处理多图存在性的 MIHBench 对照。MIOH 新增属性、关系、计数和问题模式分层。

| 假设 | 论文证据 | 证据类型 | 备择解释 |
|---|---|---|---|
| 难例暴露感知与先验脆弱性 | Table 2 比较 Easy、HP、HN | 分层行为比较 | 图像身份、选项和题目类型可能共变。CLIP 难度可携带语义先验 |
| 多图输入引入额外失分 | §4.6 / Figure 5 对相同图像比较联合输入和逐图作答 | 输入协议干预 | 问题改写、备选答案基率、分辨率、视觉 token 预算与调用次数均可能变化 |
| 能分辨感知错误和整合错误 | Figure 3 的任务×模式结果和补充 Figure V 的案例 | 描述性证据 | 总体差异无法判定某条样本的感知、算术、来源绑定或选项选择阶段 |

## 3. 方法详解

### 3.1 问题构造

1. **真值。** COCO-ReM 支持对象存在与计数，PACO 支持属性，SVG 支持空间关系。补充 §A.1.1 将计数题的源图限制在 5 个及以下对象，缓解密集计数漏标。
2. **压力。** HP 选择仍存在但较小、遮挡明显或 CLIP 相似度偏低的目标。HN 选择目标缺失、共现物或语义近邻明显的图像。NI 总体设计取 2、4、8、10 张图，§4.4 单独描述 8 图条件，Table 2 的 NI 列没有按图像数展开。
3. **题目。** 正文 §3.2 / Table 1 设计 26 种题型。对图像元数据应用存在、求和、比较或选择规则，加入干扰项与适用的弃答选项。从约 26,000 道自动构造题中，三位标注者独立检查真值、题面和选项，分歧多数投票，持续歧义时剔除。验证池约 20,000 道，再分层抽样（补充 §A.4.4）。
4. **计分。** 模型接收图像组与多选题。人工环节用于筛题和确认真值。原文主指标为正确选项的命中率。可执行的字符串规整、非法回答和多候选命中处理未公开核实。

### 3.2 关键量与计算位置

以下为本站对正文 §3.3、§4.6 与补充 §A.2 的符号化。给定图像 $I_i$、目标类别 $a$、共现类别 $b$：

$$
s(I_i,a)=\frac{v_i^\top t_a}{\lVert v_i\rVert\lVert t_a\rVert},
\qquad
\widehat P(a\mid b)=\frac{N(a,b)}{N(b)} \quad(N(b)>0).
$$

$v_i,t_a\in\mathbb{R}^d$ 分别为构造阶段的 CLIP 图像与文本嵌入。$d$ 随 CLIP 骨干而变。$N(a,b)$ 为 COCO 训练集中同时标注两类的图像数，$N(b)$ 为标注 $b$ 的图像数。低语义相似度可筛出难正例，高语义相似度或强共现可筛出难负例，阈值与配置待核。这些量仅用于候选样本构造。

对 Figure 5 中的任一图是否存在任务，$n$ 为图像数，$y_i\in\{0,1\}$ 为单图真值，$\hat y_i$ 为逐图预测。真值 $y=\bigvee_{i=1}^{n}y_i$，逐图基线 $\hat y_{\mathrm{sep}}=\bigvee_i\hat y_i$。联合预测 $\hat y_{\mathrm{joint}}$ 由多图回答取得。逐题准确率写为 $m^{-1}\sum_{j=1}^{m}\mathbf{1}[\hat c_j=c_j]$，其中 $m$ 为题数，$c_j$ 为第 $j$ 题正确选项。多选模板到布尔值的完整映射待核。逐图 OR 有累积假阳性的风险，多阳性也能弥补单次漏检，故应按全阴性、恰一阳性与多阳性分别报告。

### 3.3 实现与成本

固定评测集上的作答涉及视觉预填充和答案生成。原文报告四张 NVIDIA A6000 和温度 0。一次联合输入对比 $n$ 次逐图调用。实际图像分辨率、视觉 token 数、批处理、wall time 和峰值显存待核。两臂都没有注入 KV、缩放 head 或更新参数。要继续定位来源绑定，可固定图数、每图像素和模板后交换图号，记录每个对象的独立识别结果与最终图号、数量或关系方向。

## 4. 实验设计与关键结果

### 4.1 设置

| 项目 | 可核对内容 |
|---|---|
| 模型 | 29 个模型或配置，包括 GPT-5、Gemini-2.5 Pro、Qwen2/2.5-VL、LLaVA-Interleave、LLaVA-OneVision、InternVL3.5、MiniCPM、Mantis、Ovis2.5、Phi-4-multimodal |
| 数据 / split | 3,484 道题，论文报告覆盖 11,732 张图。未取得样本级 ID、重复图分组、分层分母或 split manifest |
| Prompt / 解码 | 正文 Table 1 给代表模板，Figures 1–2 和补充 §C 给完整样例。温度 0。系统提示、精确 checkpoint 或 API 快照、max tokens、图像预算和非法回答处理待核 |
| 指标 / 基线 | MCQ accuracy ↑，主表作横向模型比较。Figure 5 对照多图联合与逐图合并。随机和频率基线需按选项结构与题型计算 |
| 统计 | 补充 Figure II 描述跨模型离散度。主表未报告样本级配对检验、聚类置信区间或重复运行误差 |

### 4.2 主结果

以下摘自 CVF 正文 Table 2 的跨模型 Overall 行。指标均为准确率（%，↑），差值为百分点。本文贡献是评测设计，压力组差异描述条件变化。

| 设置 | Easy 对照 | 压力组 | 差值 | 来源 |
|---|---:|---:|---:|---|
| 存在性 HN | 62.4 | 51.9 | −10.5 | Table 2 |
| 存在性 HP | 62.4 | 51.5 | −10.9 | Table 2 |
| 存在性 NI | 62.4 | 30.0 | −32.4 | Table 2 |
| 计数 HN | 24.3 | 29.5 | +5.2 | Table 2 |
| 属性 HP | 37.5 | 31.3 | −6.2 | Table 2 |
| 位置 HN | 46.9 | 35.2 | −11.7 | Table 2 |

同表总准确率 36.1%，Qwen2-VL-7B 为 49.1%，Qwen2.5-VL-3B 为 44.3%。§4.4 把计数变化解释为地板效应，但计数 HP 同样高于 Easy（27.0 vs 24.3）。解释需按题核对选项数、随机命中率和类别分布。LLaVA-v1.6 的 NI 格缺值，比较模型应使用共同覆盖。

### 4.3 消融与分析实验

| 实验 | 对照与结果 | 证据边界 | 出处 |
|---|---|---|---|
| 联合多图 vs 逐图汇总 | 相同视觉内容，图中各展示模型的逐图作答准确率均更高 | 提示、作答次数、有效图像分辨率和选项基率仍可混淆。Fig. 5 标注七个模型的精确值 | §4.6 / Figure 5 |
| Easy 强度与抗压 | 高 Easy 准确率未普遍伴随更高抗压。作者报告规模与抗压关系很弱 | 商业模型规模用估计值，有限模型集合与难度构成限制外推 | §4.5 / Figure 4 |
| 代表性失败 | 相对位置例中，有模型选错对象身份，也有模型选中对象共存但关系不符的图 | 答案可按身份和关系分开标注。单例无法定位内在计算 | 补充 §C.2 / Figure V |

补充 §C.2 的深灰色碗案例讨论「所有图」，Figure V 的题面询问「任一图」，选项再区分全有、部分有和全无。复用该例时应保留完整量词语义。补充 §A.4.4 明确报告位置标注歧义及计数漏标，最终集合经过人工过滤，仍需报告被过滤的分布与一致性。

Figure 5 的存在性联合→逐图准确率包括 Gemini-2.5-Pro 90.0→95.8%、Qwen2-VL-7B 80.0→94.0%、GPT-5 78.0→93.5%。对照样本与 Table 2 全集口径不同。

### 4.4 结果解读

**论文支持。** 跨图对象问答在不同任务和压力下呈现分层差异。相同图像内容下，两种输入与作答协议也出现同方向的差距。聚合成单一准确率会掩盖计数、位置和对象身份的差别。

**证据缺口。** 逐图消融限于存在性，计数、属性和关系还缺同类对照。没有内部组件干预来定位失分。主表的 MCQ 准确率无法量化开放生成中的对象召回、长度、重复或通用能力。

## 5. 亮点与贡献

设计让「图中发生了什么」与「发生在哪张图或怎样汇总」可以分别测量。ROHE 提供同场景删对象的成对存在性对照，MIOH 提供同组图跨图聚合与来源归属的设计。它们可共用错误登记，但需要不同的提问与图像控制。

## 6. 局限、指标漏洞与审稿风险

- **代理有效性。** MCQ accuracy 混合视觉感知、图号、推理与输出格式。应加报无效输出、弃答、FP/FN。开放生成另报 recall/coverage、长度、重复和通用质量。
- **提示与共现。** 候选编排可能泄漏答案。CLIP 与共现选题可能放大特定类别或场景。文本-only、空白图、随机选项和按源数据分层可验证。
- **标注与统计。** 空间术语和遮挡下的计数容易歧义，源标注也可能漏检。未取得一致性与样本级分组。配对区间应在共享图像组或源场景层面重采样。
- **成本与迁移。** 图像尺寸、token 均分、独立调用、API 漂移会影响比较。COCO 等公开图像的训练重叠风险未得到样本级核验。
- **可复现性。** 截至 2026-11-21 未确认完整题库、评测代码或派生数据许可。补充样例支持设计审计。以下复现争议为本站从原文推导的疑问，公开评审与 rebuttal 未取得。

## 7. 与我的研究关系

个人未公开研究适配 **UNKNOWN**。此处列公开领域比较。

- **可借鉴。** real/null 可扩展为图号置换、仅增删目标数量或仅交换位置。固定问句与回答约束后，比较正确与竞争图号的 token/logit margin。POT、VR、PD、RBC 等外部支持度或反事实指标可作为候选诊断。MIOH 本身未验证这些量，尤其应在 CLIP 选题层中使用人工、非 CLIP 对照。head 与 residual 归因还需独立的组件干预和随机对照。
- **Baseline 决策。** High 为多图存在性协议与逐图 OR 基线，Medium 为来源绑定和属性/关系的 related work，Low 为可直接复算 benchmark 或缓解算法。用许可清晰的独立样本近似时，标记为协议复现。
- **公开关系。** [THRONE](throne.md) 为原文 §2 引用的开放描述对象评测。[ROHE](removed-object-hallucination-odpo.md) 是原文参考文献 [14] 的同场景删对象成对测试。三者的真值单位、采样和输出形式有差异，各自主指标需分别解释。

### 面向 CVPR 投稿的可借鉴证据

| 来源 | 可审阅证据 |
|---|---|
| 官方评审指南 | [CVPR 2027 Reviewer Guidelines](https://cvpr.thecvf.com/Conferences/2027/ReviewerGuidelines) 中的贡献、方法可靠性、经验核验和局限要求 |
| 论文实际证据 | §3.2 / Table 1 题型轴、Table 2 多模型分层、Figure 5 同图作答对照、补充 Figure V 的失败样例 |
| 本站建议 | 最近邻对照列 MIHBench、单图识别上限和语言-only。冻结图像次序、模板和视觉预算，同时记录分层配对区间、无效回答、失败分母及运行成本。发布样本 ID、答案解析、许可、模型快照和训练重叠检查 |

## 8. 可执行的后续实验

按单模型推理调用次数估计，均无需训练。视觉 token、显存和耗时另行测量。

| 实验 | 数据与对照 | 记录 | 预期与失败条件 | 成本 |
|---|---|---|---|---|
| E1 联合与逐图 | 100 组许可明确的双图存在题，原生多图小模型。联合、逐图 OR、逐图真值上限。正例数 0/1/2 分层 | Accuracy、FP/FN、无效率、token、配对 CI | 逐图差距在同模板同预算下仍成立。CI 跨零或差距在匹配后消失，则额外跨图代价未获支持 | 约 300 次推理 |
| E2 图号置换 | 100 组唯一目标图交换顺序，同步映射真值和选项，单图先验可识别 | 对象识别、源绑定、置换等变率 | 单图识别保持且错绑增加。单图也改变时，先查分辨率和预处理 | 约 400 次，含单图检查 |
| E3 单独改数量或位置 | 60 组成对图。位置组固定对象与数量、交换相对关系。计数组只改数量。另问目标是否可见 | 两端均正确、关系反转率、数量差、检测失败 | 答案跟随唯一视觉改动。若改动同时影响可识别性或背景，剔除该样本 | 约 240 次，另计人工审查 |
| E4 估计语言先验 | 80 组匹配的 HN/HP/常规样本。比较原图、尺寸匹配空白图、仅文本，置换选项 | 正确与竞争选项 margin、拒答和 FP/FN | 真实图带来方向一致的 margin 提升。若空白和文本相近，且与实图无差距，先查模板泄漏 | 约 240 次，置换复测另计 |

## 9. 复现清单

- [x] 记录 CVF 正文、独立补充和 arXiv v1。
- [x] 记录数据源、温度、题型、筛选和标注方式、Table 2 与 Figure 5。
- [ ] 冻结题库、样本 ID、代码提交、许可和原始输出。
- [ ] 补 checkpoint/API、完整 prompt、答案解析、长度与视觉 token 配额。
- [ ] 补配对区间、分层分母、随机基线、无效输出和成本。若用于生成缓解另报召回、覆盖、长度与重复。

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 直接相关性 | 5 | 显式区分存在、计数、属性和位置，可延伸到源绑定 |
| 新颖性 | 4 | 将多图问题模式与输入压力纳入同一套诊断 |
| 机制证据 | 3 | 同视觉内容的行为干预，仍有接口与预算混淆 |
| 实验完整性 | 4 | 29 个模型或配置、有分层主表及失败例，缺逐题统计 |
| 可复现性 / 低算力 | 2 | 小规模独立近似可做，完整资源与配置未核验 |
| 知识库增量 | 5 | 补上多图来源归属与逐图分解的评测入口 |

## 11. 检索标签与来源边界

- **版本。** CVF 正文和独立补充，CVPR 2026 主会，第 18295–18305 页。CVF 网页题名无连字符，PDF 题名使用 Multi-Image，作者、页码和内容对应。arXiv:2608.30653 v1 于 2026-08-31 提交，所引主表数字一致，以 CVF 为准。IEEE DOI 未核实。
- **代码和数据。** 核对正文、补充、arXiv 及题名与作者公开搜索。截至 2026-11-21 未发现可确认归属的完整代码与题库。源数据与 MIOH 派生题库的分发许可分别待核。
- **公开评审。** 截至 2026-11-21 未发现公开评审页面。正式发表身份由 CVF 书目验证。
- **图和推断。** 官方概览为 CVF 正文 Figure 1，本页仅链接原文。符号化、混淆项、评分和实验建议为本站分析。未运行实验。

---
title: "Same Attention, Different Truths: Put Logit-Lens over Visual Attention to Detect and Mitigate LVLM Object Hallucination"
description: 用 Logit Lens 检查高注意区域能否解码出目标对象，并按视觉不确定性与上下文先验两类机制进行定向缓解
authors: [Zichuan Wang, Songlin Yang, Bo Peng, Zhenchen Tang, Yang Li, Beibei Dong, Jing Dong]
venue: CVPR
year: 2026
resource_type: 方法论文
direction: Token / Logit
secondary_directions: [Attention Head / Path, Evaluation / Recall]
hallucination_type: [Object hallucination]
method_level: [Visual token, Attention, Logit-level]
training: Training-free
status: 已精读
source_status: CVPR 2026 正式论文、arXiv v1、补充材料、官方 LaTeX 素材与官方代码入口已核对
review_state: automated
arxiv_version: v1
last_verified: 2026-08-19
paper_url: https://arxiv.org/abs/2608.07302
proceedings_url: https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Same_Attention_Different_Truths_Put_Logit-Lens_over_Visual_Attention_to_CVPR_2026_paper.html
code_url: https://github.com/wzczc/SADT
overview_figure: ../assets/images/papers/same-attention-different-truths-overview.png
overview_figure_source: Figure 4 in the official arXiv v1 LaTeX source package
tags: [Object hallucination, Logit Lens, Visual attention, Training-free, CHAIR, AMBER, CVPR 2026]
---

# Same Attention, Different Truths（SADT）

<div class="paper-meta"><span>CVPR 2026</span><span>Object Hallucination</span><span>Attention + Logit Lens</span><span>Training-free</span></div>

[arXiv](https://arxiv.org/abs/2608.07302){ .kb-button .primary } [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Same_Attention_Different_Truths_Put_Logit-Lens_over_Visual_Attention_to_CVPR_2026_paper.html){ .kb-button } [官方代码](https://github.com/wzczc/SADT){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>真实对象与幻觉对象在中后层可能获得同样强的视觉注意，差别在于高注意区域的隐藏表示能否经 LM head 解码出与生成对象一致的语义；SADT 据此用 LLCC 检测，再以 HARM 区分视觉不确定与上下文先验，并对两类错误分别掩码或做 VEED 视觉证据增强解码。</p></div>

## 官方方法概览图

<figure class="paper-figure">
  <a href="../../assets/images/papers/same-attention-different-truths-overview.png" target="_blank" rel="noopener">
    <img src="../../assets/images/papers/same-attention-different-truths-overview.png" alt="SADT Detect-Mitigate 框架：LLCC 检测、HARM 分类与 VEED 解码">
  </a>
  <figcaption>官方 Detect–Mitigate 框架（论文 Figure 4）。图片由 arXiv v1 官方 LaTeX source package 中的 <code>images/framework.pdf</code> 转换；点击查看原图。</figcaption>
</figure>

图的左半部分先对生成对象词定位高注意视觉区域，并用 Logit Lens 判断区域语义与对象词是否一致；右上 HARM 掩蔽这些区域并重新生成，以“错误是否仍出现”区分 Type 1/2；只有 Type 2 再进入右下 VEED，将真实视觉区域的 logits 与掩蔽分支 logits 融合。它不是一条固定的对比解码公式，而是“在线检测 → 反事实判因 → 分支干预”。

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 研究对象 | 开放式图像描述中的对象幻觉；生成了图中不存在的名词 |
| 核心反例 | grounded 与 hallucinated object token 在 Image-Attention Stage 的注意强度相近 |
| 新诊断 | 对 top-k 高注意视觉 token 施加 Logit Lens，检查其语义与输出对象的一致性 |
| 两类机制 | Visual uncertainty：掩码后错误消失；Contextual prior：掩码后错误仍在且注意漂移 |
| 方法类型 | Training-free、token-level 在线检测与条件式缓解 |
| 主要评测 | COCO2014/CHAIR、AMBER；LLaVA-1.5、Shikra、Qwen2-VL |
| 最适合角色 | “attention quantity ≠ evidence quality”的机制证据；cause-aware mitigation baseline |

## 2. 研究背景与核心矛盾

### 2.1 论文在反驳什么

许多视觉增强或 attention reallocation 方法隐含一个叙事：幻觉发生时模型“看图不够”，所以增强 image attention 就会变好。SADT 先按层统计生成 token 对图像 token 的 attention ratio，发现非对象词几乎不看图，而对象词在中后层形成明显的 Image-Attention Stage；在 LLaVA-1.5-7B 的分析中，该阶段为第 20–27 层。关键是，真实对象和幻觉对象都能在这一阶段把注意聚到局部区域，单看 attention magnitude 很难区分真假。

这不是在证明 attention 无用，而是在缩小结论：**attention 的量或位置只告诉我们模型从哪里取信息，不保证该区域的表示真的支持输出语义。** 因此论文把判断单位从“看了多少”换成“看中的视觉表示经输出头翻译后说了什么”。

### 2.2 核心假设与证据强度

| 假设 | 论文证据 | 强度 | 仍可能的混淆 |
|---|---|---|---|
| 对象词存在稳定的图像注意阶段 | 分层 attention ratio；对象/非对象对照 | <span class="evidence-medium">统计相关</span> | 层区间可能随架构变化 |
| 幻觉关键在 evidence semantics 而非 attention quantity | 高注意区域 Logit-Lens 解码一致性 + LLCC 检测结果 | <span class="evidence-medium">诊断证据</span> | LM head 对中间视觉状态的可读性不等于因果使用 |
| 两类幻觉有不同来源 | 掩码高注意区域后的生成反事实 | <span class="evidence-high">干预证据</span> | 掩码带来 OOD 与视觉内容损失 |
| 分型干预优于统一增强 | HARM/VEED 组合在 CHAIR、AMBER 的结果 | <span class="evidence-high">输出干预</span> | 需要与等算力、等长度干预比较 |

### 2.3 “两类机制”的精确定义

Type 1 并不等于一般意义上的视觉编码错误，而是：原生成依赖一个容易混淆的局部区域，移除该区域后同一对象词不再出现。Type 2 也不是直接测得“语言模型记忆占比”，而是：移除最初证据后对象词仍出现，且 attention 转向别处；作者把这种对局部证据不敏感的持续性归因为 contextual prior。这个操作性定义很有用，但其机制名仍比观测本身更强，复现时应同时保存掩码前后候选 logits、attention drift 和对象词匹配结果。

## 3. 方法详解

### 3.1 LLCC：从注意区域读取语义

对当前 token (o_t)，论文先在 Image-Attention Stage \(\mathcal S_{IA}\) 计算平均图像注意：

\[
\mathcal A_{img}(o_t)=\frac{1}{|\mathcal S_{IA}|}\sum_{l\in\mathcal S_{IA}}\sum_{j=1}^{N_{img}}\alpha^{(l)}_{tj}.
\]

只有 \(\mathcal A_{img}(o_t)>\tau_{attn}\) 的候选进入对象检查。随后收集各层 top-k 高注意视觉 token \(\Omega_t\)，把其隐藏状态直接送入模型 unembedding \(W_U\)：

\[
v_t^i=\arg\max_{v\in\mathcal V}[\operatorname{softmax}(W_Uh(\omega_t^i))]_v.
\]

若输出对象 (o_t) 与至少一个视觉解码词 (v_t^i) 的语义相似度超过阈值，就判为真实，否则判为幻觉。实验设置为 \(\tau_{attn}=0.15\)、\(k=3\)、\(\tau_{sim}=0.8\)，语义匹配依赖 WordNet 或相似度函数。这里有三个串联 proxy：attention 选区、Logit-Lens 读出、词义匹配；任一环节失败都可能造成检测误差。

### 3.2 HARM：掩码也是分类器

对 LLCC 报警的对象词，HARM 将所有 top-k 高注意 patch 组成 mask，用均值颜色或零值替换后重新生成。如果 (o_t\notin O_{new})，记为 Type 1 / Visual Uncertainty，并直接采用掩码后的结果；若 (o_t\in O_{new})，记为 Type 2 / Contextual Prior。HARM 同时承担反事实实验、机制分类和 Type 1 缓解三项作用，设计紧凑，但也导致分类标签与所选干预耦合。

### 3.3 VEED：只处理对掩码不敏感的错误

Type 2 中，作者取最受注意视觉区域的 Logit-Lens 输出 \(z_t^{vis}=W_Uh(\omega_t^{max})\)，并与掩码图像分支的解码 logits 融合：

\[
p_t=\operatorname{softmax}((1-\alpha)z_t^{vis}+\alpha z_t^{mask}).
\]

较小的 \(\alpha\) 给真实视觉区域语义更高权重。注意这里不是“原图 logits 减去 mask logits”的经典 VCD，而是将局部视觉表示的 unembedding 与 mask branch 相加；有效性取决于局部视觉状态可经共享 LM head正确读出。

### 3.4 计算与实现边界

LLCC 要读取中间 attention 和 visual hidden states；一旦报警，HARM 至少增加一次掩码重生成；Type 2 还要运行 VEED 分支。因而 “training-free” 不等于“单次前向”。官方代码仓库截至核对日仅能确认项目入口，复现前应固定 Image-Attention Stage 的架构映射、对象 token 识别、WordNet 词形归并、mask patch 回映射和 \(\alpha\)。

## 4. 实验设计与关键结果

### 4.1 设置

| 项目 | 内容 |
|---|---|
| 检测数据 | COCO2014 随机 500 图；LLaVA-1.5-7B 生成描述；CHAIR 标注真假对象 |
| 检测对照 | Uncertainty Score、InterConf、SVAR |
| 缓解模型 | LLaVA-1.5-7B/13B、Shikra-7B、Qwen2-VL-7B（CHAIR）；前三者用于 AMBER 表 |
| CHAIR | COCO val2014 500 图；CHAIR_S/CHAIR_I 越低越好 |
| AMBER | 1004 图；CHAIR、Hal、Cog 越低，Cover 越高 |
| Baselines | Greedy/Beam/Nucleus、VCD、OPERA、DeCo、Devils、PAI |
| 资源 | 单张 NVIDIA A100 40GB；Beam=3，Nucleus top-p=0.9、temperature=0.7 |

### 4.2 主结果

| 结果（论文表号） | Baseline | SADT | 解读 |
|---|---:|---:|---|
| 检测 F1，Table 1 | SVAR 0.6842 | **0.7932** | 同时 Precision 0.7870、Recall 0.7955 |
| CHAIR，LLaVA-1.5-7B，Table 2 | PAI 29.8 / 13.2 | **26.8 / 10.0** | CHAIR_S / CHAIR_I，均越低越好 |
| CHAIR，Qwen2-VL-7B，Table 2 | PAI 24.7 / 8.6 | **24.0 / 8.3** | 跨架构增益较小但方向一致 |
| AMBER，LLaVA-1.5-7B，Table 3 | Greedy CHAIR 6.9、Hal 32.0、Cover 51.0 | **2.8、14.7、51.2** | 幻觉下降且 coverage 未下降 |

CHAIR 表中方法在四个模型上均为最低 CHAIR_S/I；AMBER 中三模型均降低 CHAIR/Hal，并保持 Cover。这个结果支持“分型干预有效”，但不单独证明作者的机制命名，因为一个更保守或更长的多分支过程也可能改变指标；好在 AMBER Cover 没有随幻觉率一起下降，削弱了纯删除解释。

### 4.3 消融与分析实验

论文最关键的分析不是单一 SOTA 表，而是三层证据链：对象词与非对象词的 layer-wise image-attention ratio 定位 Image-Attention Stage；在同样高 attention 的区域上比较 logit-lens 语义一致性以区分真实/幻觉对象；再按 HARM 的两类风险分别使用 VEED 路由。Table 1 的 detector ablation 显示 LLCC/HARM 相对 uncertainty、InterConf 和 SVAR 提升，Table 2–3 的跨模型结果说明该分型能转化为干预收益。仍缺少 random top-k patch、同 attention mass 但不同语义的 matched control，以及自动跨架构层定位消融，因此不能把 LLaVA 的第 20–27 层直接视为普适阶段。

#### 实验还缺什么

最关键的缺口是端到端成本与等算力对照：检测未报警、Type 1、Type 2 的平均额外 forward 数应分别报告。其次，应在每个模型上自动定位 Image-Attention Stage，而非默认 LLaVA 的 20–27 层。第三，LLCC 需要 random top-k、相同 attention 质量但不同语义一致性的对照，以排除只是“高注意区域更容易被 LM head读出”。最后，开放词表对象的 WordNet/相似度阈值会影响检测 F1，需要给 bootstrap CI 与 threshold transfer。

## 5. 亮点与贡献

- 把问题从 attention quantity 重构为 attended evidence quality，直接挑战一个常见但过强的解释。
- 将 Logit Lens 用在对象词对应的视觉区域，而不是只看 decoder hidden state，形成可解释的局部证据检查。
- HARM 把干预结果用作分型依据，使“检测—判因—治疗”成为连贯管线。
- 结果同时报告 CHAIR 和 AMBER Cover，至少部分控制了“删内容换低幻觉”的伪改进。
- 正式 CVPR 版本、LaTeX 图源和项目代码入口公开，方法图与核心表可追溯。

## 6. 局限、指标漏洞与审稿风险

1. **Logit-Lens 不是因果读出。** 中间视觉状态能被 (W_U) 解码，并不表示生成路径实际使用了该语义；需要 activation patching 或局部 value/output 干预验证。
2. **架构特定层段。** Image-Attention Stage 在 LLaVA 上明确为 20–27 层，Qwen/Shikra 是否采用同样定位策略需从代码确认。
3. **掩码 OOD。** 黑块/均值块既删除对象证据，也改变局部统计；应有 blur、inpainting、random-patch 与同面积对照。
4. **分型定义与治疗耦合。** “掩码后消失”被直接命名为视觉不确定，其他原因如解码随机性、对象词同义替换也可能造成消失。
5. **在线成本。** 报警后的重生成和 Type 2 额外分支可能显著增加 latency，论文未给出完整吞吐/显存 Pareto。
6. **检测标注边界。** CHAIR 只覆盖 COCO 对象集合；开放词表、属性和关系不能从本结果直接外推。

## 7. 与我的研究关系

### 7.1 可直接借鉴

这篇论文提供一条很适合接入 real/blank/counterfactual 框架的三层证据链：attention 负责定位、Logit Lens 负责读出、mask intervention 负责检验依赖。可把 LLCC score 与 (VR_t=z_t(I)-z_t(I_{blank}))、head-output divergence、residual logit contribution 并排，检查“视觉条件敏感”与“局部视觉语义一致”是否为不同维度。

### 7.2 Baseline 决策

**适合度：High。** 对象幻觉检测可先只复现 LLCC，不必实现完整重生成；缓解对比则至少实现 HARM 与 VEED 分支，并记录实际 extra forward。与 PAI/VHD 类 attention 增强相比，SADT 是“检查所看内容”；与 SID/VCD 相比，它的反事实区域由对象词 attention 动态定位。

### 7.3 不应循环定义

如果用 LLCC 生成 hallucination label，再用同一 Logit-Lens 特征训练检测器，会造成循环验证。标签应来自 CHAIR/人工标注，LLCC 只作为待评估特征；分型标签则应被称为“mask-response operational type”，不要直接当作机制真值。

## 8. 可执行的后续实验

| 实验 | Research question | Model / data | Intervention / comparison | Recorded outputs | Expected observation | Failure case | Cost |
|---|---|---|---|---|---|---|---|
| E1 Attention–truth decoupling | 等 attention 下语义一致性是否仍有效？ | LLaVA/COCO | attention-matched grounded vs hall token | LLCC、AUROC、layer curve | LLCC 仍分离 | 只反映 attention sharpness | Low |
| E2 Causal readout | Logit-Lens 语义是否真正参与生成？ | 选定对象 token | patch top region state / random region | target logit、rank、caption | 定向 patch 改变目标词 | readout 可解码但无因果力 | Medium |
| E3 Mask controls | HARM 的收益是否来自特定证据删除？ | CHAIR 500 | black/mean/blur/inpaint/random | type rate、CHAIR、Recall | 目标区域优于等面积随机 | 任意破坏都有效 | Medium |
| E4 Adaptive stage | 不同模型能否自动定位 IA stage？ | 3–4 个 LVLM | 固定层 vs data-driven layer band | LLCC F1、transfer | 自动层段更稳 | 层段依赖任务 | Medium |
| E5 Cost Pareto | 分型缓解是否值得额外计算？ | CHAIR/AMBER | SADT vs VCD/SID 等延迟 | latency、memory、CHAIR、Cover | 高风险门控更优 | 成本吞噬收益 | Medium |

## 9. 复现清单

- [x] CVPR 页面、arXiv v1、正文/补充材料与 Figure 4 图源已记录
- [x] 核心检测与 CHAIR/AMBER 表格数字已对照官方源文件
- [ ] 固定各模型 Image-Attention Stage 与 layer indexing
- [ ] 固定对象 token 识别、top-k 聚合、WordNet/相似度实现
- [ ] 记录 HARM mask 生成方式、随机种子与对象同义词判定
- [ ] 报告各类型比例、额外 forward、延迟、显存、输出长度与 coverage
- [ ] 冻结官方代码 commit；当前项目仓库已出现但实现完整度需复查

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 新颖性 | 4.5 | 从注意强度转向所注意证据的可读语义，并做分型缓解 |
| 机制证据 | 4.0 | 有掩码反事实，但 Logit-Lens 因果性与机制命名仍需加强 |
| 实验完整性 | 4.0 | 多模型、检测与缓解、coverage；缺效率和更强 mask controls |
| 可复现性 | 3.5 | 正式论文与代码入口公开；多处架构/词义实现细节敏感 |
| 与当前研究相关性 | 5.0 | 可连接 token、attention、representation 与 counterfactual logit |

## 11. 检索标签与来源边界

`requires training: no` · `inference-only: yes` · `object detector: no` · `external evaluator: no` · `interpretability: high` · `mitigation: cause-aware masking/logit fusion` · `baseline suitability: high`

本文依据 [CVPR 2026 正式页面](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Same_Attention_Different_Truths_Put_Logit-Lens_over_Visual_Attention_to_CVPR_2026_paper.html)、[arXiv:2608.07302 v1](https://arxiv.org/abs/2608.07302) PDF/LaTeX source 与[作者链接的官方仓库](https://github.com/wzczc/SADT)，核对日期为 2026-08-19。官方概览图来自论文 Figure 4 原始 `framework.pdf`。截至该日期未发现可对应本论文的 OpenReview 公开评审页；“未发现”仅是检索状态，不表示不存在非公开评审。公式、设置和数字来自论文；关于循环定义、OOD、等算力对照和后续实验属于本站分析。

---
title: "Mitigating Object Hallucination in Large Vision-Language Models via Image-Grounded Guidance"
description: MARINE 把 DETR、RAM++ 等外部视觉模型的检测结果转成 guidance prompt，并用双分支 logit guidance 抑制对象幻觉
authors: [Linxi Zhao, Yihe Deng, Weitong Zhang, Quanquan Gu]
venue: ICML
year: 2025
resource_type: 方法论文
direction: Token / Logit
secondary_directions: [External Grounding, Evaluation / Recall]
hallucination_type: [Object hallucination]
method_level: [Logit-level, Detector guidance, Dual-branch decoding]
training: Training-free
status: 已精读
source_status: arXiv v2、ICML 2025/PMLR 版本、官方 LaTeX 素材与代码链接已核对
review_state: automated
arxiv_version: v2
added_at: 2026-08-20
last_verified: 2026-08-20
paper_url: https://arxiv.org/abs/2402.08680
code_url: https://github.com/Linxi-ZHAO/MARINE
overview_figure: ../assets/images/papers/marine-overview.png
overview_figure_source: Framework figure in the official arXiv v2 LaTeX source package
tags: [MARINE, Image-grounded guidance, DETR, RAM++, Classifier-free guidance, CHAIR, POPE]
---

# MARINE：Image-Grounded Guidance

<div class="paper-meta"><span>ICML 2025</span><span>External Grounding</span><span>Logit Guidance</span><span>Training-free</span></div>

[arXiv](https://arxiv.org/abs/2402.08680){ .kb-button .primary } [Code](https://github.com/Linxi-ZHAO/MARINE){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>MARINE 用 DETR、RAM++ 等外部视觉工具把图像中的对象证据聚合成文本提示，同时运行“原始输入”与“加入 guidance”两条 LVLM 分支，再以可调 γ 混合两者 logits，让只有获得外部视觉证据的对象更容易进入输出。</p></div>

## 官方方法概览图

<figure class="paper-figure">
  <a href="../../assets/images/papers/marine-overview.png" target="_blank" rel="noopener">
    <img src="../../assets/images/papers/marine-overview.png" alt="MARINE 外部视觉工具箱和双分支 logit guidance 框架">
  </a>
  <figcaption>官方 MARINE 框架图，来自 arXiv v2 LaTeX source 的 <code>Figures/demo-lvlm.pdf</code>：外部 vision toolbox 生成对象 guidance，conditional/unconditional 两条分支通过 γ 控制生成。</figcaption>
</figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 目标 | 用额外 image-grounded evidence 缓解 object hallucination |
| 视觉工具 | DETR 与 RAM++，可扩展为多个 detector/tagger |
| 信息接口 | 检测/tag 结果聚合为文本 guidance prompt |
| 生成机制 | conditional 与 original 分支的 classifier-free-style logit mixing |
| 模型 | LLaVA、LLaVA-1.5、MiniGPT-v2、mPLUG-Owl2、InstructBLIP |
| 评测 | CHAIR、POPE、LLaVA-QA90、GPT-4V 辅助质量、延迟与显存 |
| 适合角色 | external detector upper-bound；grounding-vs-language-prior 对照 |

## 2. 研究背景与核心矛盾

LVLM 的视觉编码器通常为全局语义对齐而训练，并不等价于开放词表对象检测器。对象细节可能在 vision tower 中缺失，也可能在 projector/LLM 融合时被语言先验淹没。MARINE 的思路不是修补 LVLM 内部，而是增加一个独立视觉通道：若 detector/tagger 认为图中存在某对象，就把它显式写入 guidance prompt，再用生成概率差放大这一路信息。

这是一种工程上直接、诊断上也有价值的 external-grounding baseline。它回答的是“外部对象清单能否减少幻觉”，不能单独证明原 LVLM 的哪一层或哪类 head 出错。效果上限还受 detector recall/precision 限制：漏检会抑制真实对象，误检会把外部模型的 hallucination 注入回答。

| 主张 | 支持证据 | 关键混杂 |
|---|---|---|
| 多视觉工具能补充 LVLM 证据 | DETR、RAM++ 单独/组合消融 | 组合也增加计算和覆盖范围 |
| guidance logit 比直接拼 prompt 稳定 | integration-method ablation | 两分支成本接近双推理 |
| 减幻觉同时保留质量 | CHAIR/POPE 与文本质量指标 | detector 提供了额外监督知识 |
| γ 提供可控折中 | guidance-strength sweep | 过大 γ 会偏离用户问题、堆砌细节 |

## 3. 方法详解

### 3.1 从视觉工具到文本 guidance

给定图像，DETR 提供封闭类别的对象检测，RAM++ 提供开放词表标签。多个工具的输出经规则或小型语言模型聚合，拼成类似“focusing on the visible objects in this image: …”的 guidance prompt \(c\)。这一接口的优点是对不同 LVLM 架构通用，无需重新训练 projector；缺点是位置、数量、否定和关系信息在文本化过程中可能丢失。

### 3.2 两分支 guided generation

原始分支计算 \(p_\theta(y_t\mid v,x,y_{<t})\)，guidance 分支计算 \(p_\theta(y_t\mid v,c,x,y_{<t})\)。MARINE 的组合写为：

\[
\hat p(y_t)\propto
\frac{p(y_t\mid v,c,x,y_{<t})^\gamma}
{p(y_t\mid v,x,y_{<t})^{\gamma-1}},
\]

等价地在 log space 中线性组合两路分布。论文叙述中 \(\gamma=0\) 回到原始分支，\(\gamma=1\) 完全依赖 guidance 分支；当 \(0<\gamma<1\) 时在指令遵循与视觉对象证据间折中。实现应直接核对仓库对 logits、log-softmax 和 normalization 的处理，避免把“log probability 组合”误实现为 raw logits 不经校准的加权。

### 3.3 为什么不等于普通 prompt engineering

直接把 detector list 拼进 prompt 只运行一条分支，模型可能过度照抄或忽略它。MARINE 保留原始分支作为参照，用两路概率差选择性放大 guidance 带来的 token 变化。代价是每个生成步需要双路计算；虽然共享相同图像编码与 prefix 可能部分缓存，仍不是“零额外开销”。

## 4. 实验设计与结果审计

### 4.1 设置

论文覆盖五类 LVLM 架构，主要以 DETR+RAM++ 作为视觉工具组合。CHAIR 同时报 sentence/object hallucination 与 Recall，POPE 覆盖 random/popular/adversarial，并用 LLaVA-QA90 和 GPT-4V-assisted accuracy/detailedness 检查回答质量。附录还报告 BLEU、ROUGE-L、CIDEr、SPICE、温度、动态 γ、显存与 inference latency。

### 4.2 主结果

| 设置 / 指标（方向） | Greedy | MARINE | 变化 / 解读 | 来源 |
|---|---:|---:|---|---|
| LLaVA，COCO，CHAIRs / CHAIRi ↓ | 26.6 / 10.5 | **17.8 / 7.2** | 外部 grounding 显著降低对象幻觉 | Table 1 / Table 6 |
| LLaVA-1.5，COCO，CHAIRs / CHAIRi ↓ | 8.8 / 4.6 | **6.2 / 3.0** | 在较强 baseline 上仍改善 | Table 1 / Table 6 |
| LLaVA，POPE-MSCOCO Acc / F1 ↑ | 54.2 / 68.5 | **72.2 / 76.4** | Yes ratio 95.5%→66.9% | Table 4 |
| mPLUG-Owl2，POPE-MSCOCO Acc / F1 ↑ | 76.7 / 80.4 | **85.5 / 85.0** | Yes ratio 68.2%→46.5% | Table 4 |
| LLaVA，延迟 ms/token ↓ | Greedy 26.3 | 52.2 | 1.98×，包含外部视觉模型 | Table 5 |

从研究设计看，最有价值的不是某个单表 SOTA，而是三组对照：DETR vs RAM++ vs 联合；直接 prompt/integration 方式对比；γ sweep。它们表明覆盖互补的视觉工具通常优于单个模型，且过强 guidance 会生成与问题无关的图像细节。论文也加入 MARINE-Truth，把 ground-truth object information 当作 guidance，近似表示外部证据完美时的上限。

### 4.3 消融与分析实验

| 实验 | 对照 / 唯一变量 | 关键结果 | 能支持什么 | 仍不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 外部模型组合 | DETR-only、RAM++-only、联合 | LLaVA CHAIRs：27.6 / 29.0 / **17.8**；CHAIRi：8.4 / 9.1 / **7.2** | 两类视觉工具提供互补证据 | 联合也增加覆盖面与算力，非纯算法协同 | Table 6 |
| 集成规则 | intersection vs union | LLaVA 17.8/7.2 vs 30.4/9.7；不同模型上并非所有指标都由 intersection 最优 | 一致性过滤可抑制 noisy labels | 不能推为所有 detector 组合都应取交集 | Table 7 |
| guidance strength | γ 从 0 到 1 | 幻觉先下降，但过强时 Recall/相关性受损 | 存在 hallucination–coverage Pareto | 曲线最优点依模型变化 | Figure 3 |
| Oracle guidance | MARINE vs MARINE-Truth | Truth 在 POPE 多数设置仍更高 | 外部识别质量构成方法上限 | oracle gap 不等于 detector error 的唯一贡献 | Table 2 |

需要谨慎比较不同 baseline：LURE/Woodpecker 属于输出后校正，VCD/OPERA 属于 decoding intervention，MARINE 则使用额外 detector。即使它们都“training-free”，外部模型参数、显存、预处理与双分支成本不同。公平表应同时列出 detector 参数量、图像前处理时间、首 token 延迟和每 token 延迟。

## 5. 亮点与贡献

- 把任意 detector/tagger 通过文本接口接入 LVLM，对架构侵入小。
- 通过双分支分布控制，而非无条件相信外部对象清单。
- 同时报告 CHAIR Recall 与文本质量，主动暴露“少说即少错”的风险。
- MARINE-Truth 提供外部 grounding 上限，有利于区分 detector error 与 fusion error。
- 附录对动态 guidance、sampling temperature、显存和 latency 有较完整审计。

## 6. 局限、指标漏洞与审稿风险

1. **外部错误会传播。** detector/tagger 的 false positive 可直接成为强 guidance，开放词表标签也有同义词与阈值问题。
2. **双分支推理成本。** 方法与 contrastive decoding 一样需要两路 logits，另有 detector 前处理；不能只强调无需训练。
3. **对象清单不是场景图。** 数量、属性、关系、空间和否定难由标签列表表达。
4. **评测存在共享先验。** COCO 类别、DETR 训练类别与 CHAIR 对象词表重叠，可能放大闭集优势。
5. **指令相关性风险。** 大 γ 容易把所有检测对象写进答案，即便用户只问一个局部问题。
6. **归因边界。** 成功说明外部证据有用，不说明 LVLM 内部视觉表征本来不可用。

## 7. 与我的研究关系

MARINE 可作为 internal-mechanism 方法的强外部参照。若 VR/PD/RBC 已正确识别对象，而 MARINE 仍提升，问题可能在 token selection；若内部信号缺失但 detector 有效，则是视觉编码/融合缺口。还可将 detector confidence 与内部 risk score 共同用于门控：仅在内部视觉依赖低且外部证据高时开启第二分支，降低成本和误导风险。

**Baseline 适合度：High（external grounding 组），Medium（统一算力表）。** 代码公开、无需训练，但要安装两套视觉模型并支付双分支推理。

## 8. 可执行的后续实验

| 实验 | 问题 | 比较 | 指标 | 失败解释 | 成本 |
|---|---|---|---|---|---|
| E1 Error propagation | 外部 false positive 如何传入？ | 人工注入/删除 tags | token logit、CHAIR | guidance 被无条件复制 | Low |
| E2 Closed-set audit | 收益是否来自 COCO 类别重叠？ | in-/out-of-vocabulary objects | precision/recall | 对开放类别无效 | Medium |
| E3 Risk gate | 能否只在高风险步启用？ | always-on vs VR-gated | CHAIR、latency | 门控漏掉早期错误 | Medium |
| E4 Evidence format | 文本清单是否损失结构？ | list vs boxes/counts/scene graph | attribute/relation | 文本化是瓶颈 | Medium |
| E5 Cost Pareto | 相对 VCD/OPERA 是否划算？ | 同硬件同长度 | tokens/s、VRAM、质量 | detector+双分支过重 | Low |

## 9. 复现清单

- [x] arXiv v2、ICML 版本、官方方法图与代码链接已核对
- [ ] 固定 DETR/RAM++ checkpoint、类别映射、置信阈值和聚合模板
- [ ] 核对 γ 的 log-probability 实现与 KV-cache 复用方式
- [ ] 对 CHAIR 报 Recall、caption length、对象覆盖与同义词映射
- [ ] 单独记录 detector、首 token 与每 token latency/显存
- [ ] 加入外部误检注入和 OOD 对象测试

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 新颖性 | 3.5 | 将多视觉工具与 classifier-free-style guidance 结合 |
| 机制证据 | 3.0 | 工程因果链清晰，但不解释 LVLM 内部原因 |
| 实验完整性 | 4.5 | 多模型、指标、质量、成本与扩展分析丰富 |
| 可复现性 | 4.0 | 代码公开，外部 checkpoint/阈值仍需锁定 |
| 与当前研究相关性 | 4.0 | 是内部机制路线的重要外部参照 |

## 11. 检索标签与来源边界

`requires LVLM training: no` · `external detector/tagger: yes` · `dual decoding: yes` · `object-focused: yes` · `closed-set overlap risk: high` · `baseline suitability: high`

本页依据 [arXiv:2402.08680 v2](https://arxiv.org/abs/2402.08680)、ICML 2025/PMLR 正式版本、官方 LaTeX source 与 [MARINE 代码仓库](https://github.com/Linxi-ZHAO/MARINE)，核对日期为 2026-08-20。方法图来自官方 source；本文对结果的表述以机制和对照为主，使用前仍应按目标 checkpoint、prompt 与 γ 复跑，而不跨论文直接比较 SOTA 数字。

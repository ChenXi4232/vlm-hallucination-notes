---
title: "PatchGate: Narrowing the Verbalization Gap with Intrinsic Object Inventories in Frozen Vision-Language Models"
description: 从无提示视觉 patch 隐状态读取对象清单，再以包含—排除双向 logit 编辑同时约束对象遗漏与幻觉
authors: [Jihyung Ko, Eunji Jung, Hyeongsub Kim, Ziseok Lee, Jae Won Cho, Sanghyun Jo, Kyungsu Kim]
venue: arXiv
year: 2026
resource_type: 方法论文
direction: Token / Logit
secondary_directions: [Representation / Activation, Evaluation / Recall Trade-off]
hallucination_type: [Object hallucination, Object omission]
method_level: [Patch-level, Logit-level]
training: Training-free
status: 已精读
source_status: arXiv v1 正文与完整附录已核对；作者主页标注 Under Review；截至核对日未发现公开代码或公开评审页面
review_state: automated
arxiv_version: v1
added_at: 2026-09-05
last_verified: 2026-09-05
paper_url: https://arxiv.org/abs/2608.21819
overview_figure: ../assets/images/papers/patchgate-overview.svg
overview_figure_source: 本站依据 arXiv v1 Sections 3.1–3.2 制作的等价抽象；不是论文官方 Figure 2
tags: [PatchGate, VEX, VIED, Logit lens, Object inventory, Coverage, CHAIR, AMBER, POPE, Training-free]
---

# PatchGate

<div class="paper-meta"><span>arXiv v1 · Under Review</span><span>Patch / Logit</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2608.21819){ .kb-button .primary } [作者公开页面](https://shjo-april.github.io/){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>PatchGate 在生成前用一次 image-only forward，把后 1/3 decoder layers 的视觉 patch 隐状态经 unembedding 读成对象证据清单；生成时一边提升“有证据但尚未说出”的对象，一边压低“语言 logit 高但视觉证据弱”的对象，在 AMBER 上把 Cover 49.4→56.0、CHAIR 7.5→6.6，但 Hal 31.4→34.3，说明它改善的是对象提及级 precision–coverage 平衡，而非所有幻觉指标。</p></div>

## 官方方法概览图

<figure class="paper-figure">
  <a href="../../assets/images/papers/patchgate-overview.svg" target="_blank" rel="noopener"><img src="../../assets/images/papers/patchgate-overview.svg" alt="本站对 PatchGate 的等价流程抽象：VEX 构造对象清单，VIED 双向修改 logits"></a>
  <figcaption><strong>本站等价抽象，不是作者原图。</strong>依据 <a href="https://arxiv.org/abs/2608.21819">arXiv v1</a> Sections 3.1–3.2 绘制。论文官方 Figure 2 展示完整 pipeline，但当前公开页面未给出足够明确的单图再分发许可边界，因此本站不复制原图；实现判断以正文公式为准。</figcaption>
</figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 研究对象 | 开放式 caption 的对象 hallucination 与 omission；二元 object-existence QA |
| 核心归因 | 冻结 VLM 内部可读出的对象证据与最终 verbalization 不一致 |
| 方法类型 | inference-time、training-free、detector-free |
| 干预位置 | image-token hidden states 的 logit-lens readout；next-token logits |
| 外部依赖 | WordNet physical-object 单 token 词表；无需外部 detector/LLM evaluator |
| 主要评测 | AMBER generative/discriminative、POPE random/popular/adversarial |
| 最适合角色 | recall/coverage-preserving decoding baseline；patch-to-vocabulary evidence probe |

## 2. 研究背景与核心矛盾

### 2.1 研究的 hallucination

论文限定在**对象级可靠性**。开放式 caption 中，unsupported object mention 是 hallucination，已标注可见对象未被提及是 omission；二元 QA 中分别对应 absent-object false positive 与 present-object false negative。它没有把 attribute、relation、counting 或 reasoning error 混入主张，因此 AMBER 的 Cover/CHAIR 是最贴合目标的主指标，Hal/Cog 只是补充诊断。

### 2.2 现有方法的缺口

多数 training-free 方法只在对象词已经接近生成时抑制风险 token，能降低错误提及，却无法召回模型从未打算说出的可见对象。外部 detector/tagger 能补对象，但把性能上限绑定到外部词表与检测器。PatchGate 的问题重构是：先问冻结 VLM 在**任何 caption prompt 之前**已经编码了哪些对象，再把这个 intrinsic inventory 与逐步生成意图对齐。

### 2.3 核心假设与证据强度

| 假设 | 论文证据 | 证据类型 | 仍可能的混淆因素 |
|---|---|---|---|
| late-layer patch states 可读出对象证据 | 未提及对象的 PCS 对 omission AUROC .890；已提及对象的 $1-PCS$ 对 hallucination AUROC .883 | 预生成相关性诊断 | unembedding 可读性不等于对象被模型因果使用；WordNet/标注闭集影响标签 |
| “证据—提及差”可统一两类错误 | ESI 单独提高 Cover，EDE 单独降低 CHAIR，组合兼顾两者 | 组件干预 | 直接 boost/suppress 对象 token 本身即可改变指标，不证明修复了视觉表征 |
| 内部 inventory 优于外部 tagger | 在同一 VIED 下 VEX 相比 GroundingDINO/RAM++ 有更高 Cover、更低 CHAIR | 替换式对照 | 外部模型的阈值、词表与别名映射未必达到各自最优 |
| 方法能跨 backbone | LLaVA-7B/13B、Qwen2.5-VL-7B、InstructBLIP-7B 的 Cover↑且 CHAIR↓ | 跨架构结果 | 主表只覆盖 AMBER；无多 seed/CI 或显著性检验 |

## 3. 方法详解

### 3.1 整体流程

```mermaid
flowchart LR
    I[图像 I] --> F[一次 image-only forward]
    F --> H[后 1/3 decoder layers 的 patch states]
    H --> U[RMSNorm + frozen unembedding]
    U --> P[PCS: layer/patch 最大对象概率]
    P --> T[自适应阈值得到对象清单 T(I)]
    T --> ESI[ESI: 提升有证据且未提及对象]
    P --> EDE[EDE: 压低高语言 logit/低视觉证据对象]
    G[基础 next-token logits] --> ESI
    G --> EDE
    ESI --> O[更新 logits 后继续解码]
    EDE --> O
```

### 3.2 关键量与公式

对 decoder layer $\ell$、视觉 patch $p$ 的 hidden state $h_p^{(\ell)}$，VEX 用冻结 LM 的归一化和 unembedding 读取 token $v$：

$$
q_p^{(\ell)}(v)=\operatorname{softmax}\!\left(W_U\operatorname{RMSNorm}(h_p^{(\ell)})\right)[v].
$$

在 WordNet physical-object 单 token 集 $V_{obj}$ 中收集各 patch/layer 的 top-1 候选。对象 $c$ 的 patch-confidence score 取选定层与 patch 上的最大值：

$$
PCS(c)=\max_p\max_{\ell\in L}q_p^{(\ell)}(c).
$$

LLaVA-v1.5-7B 默认有 $N=576$ 个视觉 patches、32 层 decoder，$L=\{22,\ldots,32\}$。将 PCS 排序后取最大相邻间隔的中点 $\theta_{TTD}(I)$，再与固定下限 $\tau_{floor}$ 取较大者：

$$
T(I)=\{c\in C(I):PCS(c)>\max(\theta_{TTD}(I),\tau_{floor})\}.
$$

VIED 在每步基础 logits $g_t$ 上做双向编辑。ESI 用对象占据 patch 的归一化比例 $e(c)$ 提升尚未生成的 inventory 对象；EDE 用“高于词表中位数的 verbalization excess”乘视觉缺口：

$$
\Delta_t^-(c)=\operatorname{ReLU}(g_t[c]-\operatorname{median}_v g_t[v])\,(1-PCS(c)).
$$

因此对象 token 的更新可等价写为：若 $c\in T(I)$，加 $\alpha_{esi}e(c)\mathbf 1[c\notin M_{<t}]$；所有 $c\in V_{obj}$ 都减 $\gamma_{ede}\Delta_t^-(c)$；非对象 token 不变。默认 caption 设置为 $\alpha_{esi}=8$、$\gamma_{ede}=0.5$，inventory floor 为 0.93（Appendix A/D）。

### 3.3 实现细节

- VEX 只做一次无文本、无输出 token 的 image-only forward；任务 prompt 在 inventory 建立后才进入生成。
- caption 与 binary QA 使用不同 VIED 路径；QA 根据 query 对象是否在 inventory 内校准 Yes/No logits。
- generative captioning 使用 AMBER 官方 “Describe this image.”；POPE 使用 “Is there a {object} in the image? Please answer this question with one word.”。
- 默认 deterministic greedy decoding；随机 baseline 固定 seed 42、temperature 1.0。论文未报告多 seed 方差。
- LLaVA-7B 单图时间 2.92s→3.30s（1.13×），peak VRAM 14.6→14.9GB；无需训练或额外参数。
- 公开论文称“submitted code archive”含实现，但截至 2026-09-05 未发现可公开访问的官方代码仓库或 commit，复现性因此仍受限。

### 3.4 方法究竟改变了什么

PatchGate 直接改变对象词的**出现倾向**，而不是证明视觉 encoder 的表示变正确。ESI 能主动增加对象提及，EDE 则抑制视觉证据弱的对象候选；这会同时改变 caption 内容密度、长度、局部语法与重复风险。其最强证据是 precision–coverage 双轴均改善，而不是“PCS 是真实因果视觉证据”。要把后者立为机制结论，还需要 real/null/object-removed image 下的 PCS 反事实、patching 与随机词表对照。

## 4. 实验设计与关键结果

### 4.1 设置

| 项目 | 内容 |
|---|---|
| Models | LLaVA-v1.5-7B/13B、Qwen2.5-VL-7B、InstructBLIP-7B；主比较为 LLaVA-v1.5-7B |
| Datasets / splits | AMBER generative 1,004 张图；AMBER discriminative；POPE random/popular/adversarial |
| Metrics | Cover、CHAIR、Hal、Cog；Accuracy、Precision、Recall、F1；AUROC/AUPRC；时间与 VRAM |
| Baselines | OPERA、VCD、Devils-in-the-Middle、MARINE、ProjectAway、ILVAD、SHIELD；GroundingDINO、RAM++ inventory |
| Ablations | ESI/EDE、layer range、max/mean aggregation、阈值、强度、词表、外部 inventory、backbone、效率 |
| Statistical evidence | 未报告 seed 方差、置信区间或显著性检验；检测 AUPRC 以 positive rate 为随机基线 |

### 4.2 主结果

| 设置 / 指标（方向） | Baseline | PatchGate | 变化 | 来源 |
|---|---:|---:|---:|---|
| LLaVA-1.5-7B，AMBER Cover ↑ | 49.4 | 56.0 | +6.6 pt / +13.4% relative | Table 2 |
| LLaVA-1.5-7B，AMBER CHAIR ↓ | 7.5 | 6.6 | −0.9 pt / −12.0% relative | Table 2 |
| LLaVA-1.5-7B，AMBER Hal ↓ | 31.4 | 34.3 | **+2.9 pt，退化** | Table 2 |
| LLaVA-1.5-7B，AMBER QA P/R ↑ | 92.5 / 62.9 | 93.8 / 66.0 | +1.3 / +3.1 pt | Table 2 |
| LLaVA-1.5-7B，POPE Avg Acc/F1 ↑ | 82.0 / 80.4 | 89.8 / 89.6 | +7.8 / +9.2 pt | Table 3 |

最重要的边界是：PatchGate 并非所有 AMBER 指标都更好。Full ESI+EDE 的 CHAIR 优于 vanilla、Cover 最高，但 Hal 比 vanilla 更差；这与 caption 中主动加入更多对象、使“任一错误即记 1”的 sentence-level 指标更容易触发一致。

### 4.3 消融与分析实验

| 实验 | 对照 / 唯一变量 | 关键结果 | 能支持什么 | 仍不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 预生成诊断 | random vs PCS/$1-PCS$ | hallucination AUROC/AUPRC .883/.707；omission .890/.705 | PCS 能排序两类对象错误 | 未做跨数据校准与 CI | Table 4 |
| inventory 来源 | GroundingDINO/RAM++ vs VEX，共用 VIED | 外部最佳 Cover 51.3、CHAIR 7.2；VEX 56.0/6.6 | 内部清单在该协议更适配 | 外部阈值与同义词公平性 | Table 5 |
| 双组件 | vanilla / ESI / EDE / full | Cover 49.4/54.8/50.3/56.0；CHAIR 7.5/6.7/6.2/6.6 | ESI 主召回、EDE 主抑制 | full 不是 CHAIR 最优 | Table 6 |
| 跨 backbone | 四个 frozen VLM | Cover 全部提高 0.7–6.6 pt，CHAIR 降 0.5–0.9 pt | 趋势不只在一个模型 | 幅度在 InstructBLIP 很小 | Table 7 |
| 强度扫描 | $\alpha_{esi}$、$\gamma_{ede}$ | 增大 ESI 推高 Cover；EDE 过强时 CHAIR 反升至 7.0 | 存在可解释 trade-off | 超参是否跨域稳定 | Table E |
| 语言质量 | perplexity/repetition/length | 论文报告有限变化，但主动 boost 会改变措辞 | 作者意识到生成副作用 | 无盲人工偏好与长文本评测 | Table G |
| 成本 | vanilla vs PatchGate | 2.92s→3.30s；14.6→14.9GB | 单额外 forward 成本较小 | 不同硬件/batch/KV 下吞吐 | Table H |

### 4.4 结果应该如何解读

**论文能够支持：**在 AMBER/POPE 的对象闭集协议上，使用冻结模型内部 patch readout 构造清单，并对对象 logits 做包含—排除编辑，可以在多个 backbone 上同时改善 mention-level CHAIR 与 object coverage；预生成 PCS 对遗漏/幻觉有较强排序能力。

**论文不能据此证明：**PCS 等于真实视觉因果贡献；方法对属性、关系、counting、reasoning 或长描述有效；相同阈值可跨数据域部署；提升不是对象词表、metric-aligned editing 或 caption 内容重分配的结果。

## 5. 亮点与贡献

- 明确把 hallucination 与 omission 视为同一 evidence–verbalization residual 的两个方向，避免只做保守抑制。
- pre-generation inventory 与 step-wise logits 分工清楚：诊断信号可独立评估，干预组件可分别消融。
- 与 GroundingDINO/RAM++ 在相同 VIED 下比较，能区分“对象来源”与“解码编辑”的贡献。
- 同时报告 Cover、CHAIR、Precision、Recall、Hal/Cog、效率和部分语言质量，信息比只给 hallucination rate 完整。

## 6. 局限、指标漏洞与审稿风险

1. **Proxy validity：**unembedding 对象词概率是可读性 proxy；没有 patching/ablation 证明相应 patch state 在生成中被使用。
2. **Language-prior confound：**WordNet 对象词与 LM vocabulary 预先对齐，PCS 可能部分反映词频/词形，而不是纯视觉证据。
3. **Annotation noise：**AMBER 未穷尽的可见对象可能被 CHAIR/Hal 误罚。论文 Figure C 也展示了该问题。
4. **Metric-aligned editing：**只编辑单 token physical-object vocabulary，与 CHAIR/POPE 的对象评测高度同构；这不代表一般视觉忠实度。
5. **Length/quality：**ESI 主动补对象，可能增加 caption 长度、列表化、重复或减少属性修饰；现有自动质量检查不足以排除。
6. **统计不足：**无多 seed、CI、显著性检验；0.5–0.9 pt 的跨模型 CHAIR 改善可能不稳定。
7. **跨模型边界：**Qwen/InstructBLIP 结果证明趋势，但默认层区间和词表读出规则是否同等适配并未充分展开。
8. **开放词表限制：**单 token WordNet physical-object vocabulary 漏掉多词实体、细粒度类别和非英语对象。
9. **外部 evaluator：**主指标无需 LLM judge，这是优点；但也受规则化 noun/object mapping 约束。
10. **公开复现：**论文提到 submitted code archive，公开作者页只有 PDF/arXiv 链接；截至核对日无法核对代码实现与 commit。

## 7. 与我的研究关系

### 7.1 可直接借鉴

VEX 可作为 POT/VR/PD/RBC 的内部对照：同一对象分别记录 patch-level PCS、real-vs-null logit gap、对象 onset 前的 chosen-logit/rank 与 grounding 标签。尤其应测试 PCS 在 object-removed counterfactual 中是否下降；如果不下降，说明它更多是 lexical decodability，而非图像中特定对象的因果证据。

### 7.2 Baseline 决策

**适合度：High（论文价值）/ Medium（立即复现）。**它直接针对 recall-preserving mitigation，主干只需一次 image-only forward 与 logits processor，理论上适合单机低算力；但官方代码尚未公开，WordNet 单 token 词表、image-only input 模板和阈值细节需要从附录自行实现，短期复现风险高于 M3ID/RSP。

### 7.3 与已有路线的差异

SADT 读取“被 attention 选中的区域能否语义解码”，PatchGate 先建立全图对象 inventory；VISOR 用 real/null margin 判断视觉增量的方向，PatchGate 用单图 late-layer 最大 readout；MARINE 借外部 detector/tagger，PatchGate 用 target VLM 自身证据。它与候选 ranker 路线互补：VEX 提供候选覆盖，EDE/其他 ranker 决定是否保留。

## 8. 可执行的后续实验

| 实验 | Research question | Model / data | Intervention / comparison | Recorded outputs | Expected observation | Failure case | Cost |
|---|---|---|---|---|---|---|---|
| E1 PCS 反事实效度 | PCS 是否随对象真实存在而变化？ | LLaVA-7B；100 对原图/对象移除图 | 同对象 real vs removed PCS | ΔPCS、AUROC、paired CI | grounded 对象 PCS 显著下降 | readout 对编辑不敏感 | Low，约 200 次 prefill |
| E2 信号横评 | PCS 是否补充 POT/VR/PD/RBC？ | CHAIR 200 图 | PCS、real/null Δlogit、POT 单独/组合 | AUROC/AUPRC、相关性、校准 | 组合优于单信号 | 信号高度同源无增量 | Low–Medium |
| E3 最小 VIED | 双向编辑能否保 recall？ | AMBER 200 图 | vanilla、ESI、EDE、full；固定 grid | CHAIR/Cover/length/repetition | full 进入左上象限 | ESI 只以更长输出换 Cover | Medium |
| E4 随机词表对照 | 收益是否来自任意 token boost？ | 同上 | WordNet inventory vs 频率匹配随机名词 | 指标与语言质量 | 随机对照明显更差 | 任何 noun boost 都提高 Cover | Low |
| E5 onset-local 版本 | 全程 logits edit 是否不必要？ | CHAIR 200 图 | always-on vs noun-onset gated VIED | CHAIR/Recall/latency/Fix-Break | 局部门控保留收益且少副作用 | 错误在 onset 前已写入状态 | Medium |

## 9. 复现清单

- [x] arXiv v1（2026-08-22）正文、Appendices A–E、Tables 2–H 已核对
- [x] 作者公开页面的 Under Review 状态已核对
- [ ] 官方代码仓库、公开 archive 与 commit（截至 2026-09-05 未发现）
- [ ] 固定 image-only conversation template、WordNet 版本与 token filtering
- [ ] 复算 largest-gap cutoff、$\tau_{floor}$、ESI/EDE 默认强度
- [ ] 记录 caption length、repetition、distinct-n 与盲人工质量
- [ ] 对 0.5–0.9 pt CHAIR 差异做 paired bootstrap / multi-seed 验证

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 与主线直接相关性 | 5 | 明确优化 hallucination–omission/coverage 双轴 |
| 方法/理论新颖性 | 4 | pre-generation intrinsic inventory + 双向 VIED 组合清晰 |
| 机制证据强度 | 3 | 有诊断与组件干预，但缺反事实和 causal patching |
| 实验完整性 | 4 | 指标、消融、外部对照、跨 backbone、效率较完整；无统计检验 |
| 可复现性/低算力适配 | 3 | 单额外 forward 较轻，但公开代码缺失 |
| 相对知识库新增信息 | 5 | 首个明确以对象遗漏召回约束 training-free 解码的 Note |

## 11. 检索标签与来源边界

`requires training: no` · `inference-only: yes` · `detector: no` · `external evaluator: no` · `interpretability: proxy-level` · `mitigation: bidirectional` · `baseline suitability: high/medium implementation risk`

本文依据 2026-09-05 核对的 [arXiv:2608.21819 v1](https://arxiv.org/abs/2608.21819) 正文与完整附录整理；作者主页将论文列为 Under Review，这不是录用证据。截至该日未发现公开 OpenReview/评审页面或可访问的官方代码仓库，论文所称 submitted code archive 不能视为公开代码。所有数值来自 v1 Tables 2–H；Mermaid、SVG 流程图、与 POT/VR/PD/RBC 的联系及后续实验均为本站分析。

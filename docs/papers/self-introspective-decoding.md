---
title: "Self-Introspective Decoding: Alleviating Hallucinations for Large Vision-Language Models"
description: 用 LVLM 自身识别低重要度视觉 token，并构造上下文相关的幻觉对比分支
authors:
  - Fushuo Huo
  - Wenchao Xu
  - Zhong Zhang
  - Haozhao Wang
  - Zhicheng Chen
  - Peilin Zhao
venue: arXiv
year: 2024
resource_type: 方法论文
direction: Token / Logit
hallucination_type:
  - Object hallucination
  - Attribute hallucination
method_level:
  - Visual token
  - Logit-level
training: Training-free
status: 已精读
source_status: arXiv 元数据已核对；最终 venue 待更新
paper_url: https://arxiv.org/abs/2408.02032
tags:
  - Self-introspective decoding
  - Visual token
  - Contrastive decoding
  - Training-free
  - CHAIR
  - POPE
---

# 知识库条目：Self-Introspective Decoding（SID）

<div class="paper-meta"><span>arXiv 2024</span><span>方法论文</span><span>Visual Token / Logit</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2408.02032){ .kb-button }

## 核心问题

*Self-Introspective Decoding: Alleviating Hallucinations for Large Vision-Language Models* 研究的是 LVLM 在图像描述与视觉问答中产生的视觉不一致幻觉，主要包括不存在物体、错误属性、位置和关系描述。论文关注的不是重新训练模型，而是如何在解码阶段抑制与图像不一致的 token。它特别批评 VCD、ICD 等 contrastive decoding 方法：通过加噪图像、遮蔽图像或 negative prompt 构造“更容易幻觉”的分支，可能引入与当前图像和文本无关的 uncertainty noise，并且通常需要额外 forward，推理成本较高。

## 方法一句话概括

SID 利用 LVLM 自身 attention 在早期 decoder 层判断哪些 vision tokens 对当前生成最不重要，只保留这些 least important vision tokens 构造一个更容易产生“上下文相关幻觉”的 contrastive branch，再用原始 logits 减去该分支 logits，从而压低 hallucination tokens。

---

## 关键公式与直观理解

### 1. LVLM 正常 next-token 分布

在第 \(t\) 个生成步，LVLM 根据图像 tokens \(v\)、文本 instruction \(x\) 和已生成 tokens \(y_{<t}\) 预测下一个 token：

\[
p(y_t \mid v, x, y_{<t})
=
\mathrm{softmax}
\left(
\mathrm{logit}_{\theta}(y_t \mid v, x, y_{<t})
\right)
\]

这里的关键是：正常分支使用完整视觉信息 \(v\)。如果模型真正依赖图像，grounded token 应该在这个分支中获得更高 logit。

### 2. Vision token importance score

SID 在第 \(i\) 个早期 decoder layer 读取 self-attention matrix：

\[
A_i \in \mathbb{R}^{B \times H \times N \times N}
\]

其中 \(B\) 是 batch size，\(H\) 是 attention heads 数量，\(N\) 是总 token 数。论文用当前生成位置对每个 vision token 的 attention 来估计其重要性：

\[
Score_i(v_j)
=
\frac{1}{H}
\sum_{h=1}^{H}
A_i^{(h)}[-1, v_j]
\]

含义是：看当前最后一个 token / 当前生成位置，在所有 heads 上平均后，对第 \(j\) 个 vision token 分配了多少 attention。

- \(Score_i(v_j)\) 高：当前生成更依赖这个 vision token；
- \(Score_i(v_j)\) 低：当前生成几乎不看这个 vision token。

SID 的反直觉点在于：它不是保留高分 tokens，而是保留低分 tokens。

\[
v_{\mathrm{low}}
=
\operatorname{BottomK}_{v_j}
Score_i(v_j)
\]

论文常用设置是保留 top 10% least important vision tokens。对 LLaVA-1.5、Shikra、LLaVA-NeXT，通常在 decoder layer \(i=3\) 选择；对 InstructBLIP，通常在 \(i=5\) 选择。

### 3. 用 least important vision tokens 构造弱视觉分支

SID 构造两个分支：

**正常分支：**

\[
l_{\mathrm{orig}}
=
\mathrm{logit}_{\theta}(y_t \mid v, x, y_{<t})
\]

**弱视觉 / hallucination-amplified 分支：**

\[
l_{\mathrm{low}}
=
\mathrm{logit}_{\theta}(y_t \mid v_{\mathrm{low}}, x, y_{<t})
\]

其中 \(v_{\mathrm{low}}\) 只包含当前上下文下 least important vision tokens。

这个分支不是 blank image，也不是 random noise。它仍来自同一张图像，并且 token selection 是由当前 instruction 和已生成文本动态决定的。因此它保留了弱视觉上下文，但去掉了当前生成最需要的关键视觉证据。这样模型更容易依赖语言共现先验，生成“看起来合理但图像中未必存在”的候选词。

例如上下文是：

> Two persons are playing ...

完整视觉分支可能根据球拍、场地等证据生成 `tennis`；而弱视觉分支缺少关键视觉 token，可能更容易提高 `football`、`basketball`、`baseball` 等共现词的 logit。这种 hallucination 不是随机的，而是与当前上下文相关的 vision-and-text association hallucination。

### 4. Contrastive decoding 公式

SID 最终用 contrastive decoding 得到校正后的 logits：

\[
l_{\mathrm{SID}}
=
(1+\alpha) l_{\mathrm{orig}}
-
\alpha l_{\mathrm{low}}
\]

其中 \(\alpha\) 控制 contrastive strength。

直观解释：

- 如果某 token 在完整视觉分支高、在弱视觉分支低，说明它更依赖真实视觉证据，应被保留；
- 如果某 token 在弱视觉分支也很高，说明它可能主要来自语言先验或上下文共现，应被压低；
- 如果 hallucinated object token 被弱视觉分支放大，subtract 后它会被抑制。

这与我的 real image vs blank image 反事实实验高度相似，但 SID 的反事实更细粒度：

\[
\text{SID gap}
=
l_{\mathrm{orig}}
-
l_{\mathrm{low}}
\]

可以理解为：

\[
\text{完整视觉证据}
-
\text{上下文相关但关键证据缺失的弱视觉证据}
\]

---

## 我需要重点理解的点

SID 最容易混淆的是：为什么 least important vision tokens 能帮助降低 hallucination。关键在于，SID 不是要用这些 token 得到正确答案，而是要用它们构造一个“有意义的错误分布”。如果完全移除图像或使用空白图像，模型可能退化成纯语言模型；如果使用噪声图像，可能引入无关不确定性。SID 保留的是同一图像中当前上下文认为不重要的 tokens，因此分支仍然与图像和文本有弱联系，但缺失了关键 grounding evidence。这种分支更容易暴露模型在视觉证据不足时会依赖哪些语言先验。

因此，SID 的逻辑不是：

\[
\text{least important tokens} \Rightarrow \text{better vision}
\]

而是：

\[
\text{least important tokens}
\Rightarrow
\text{context-aware weak vision}
\Rightarrow
\text{amplified hallucination logits}
\Rightarrow
\text{subtract hallucination-prone distribution}
\]

---

## Benchmark / Metric

论文主要在 CHAIR、POPE、GPT-4 assisted SHR、MME、MMBench、GPT-4V assisted evaluation 等设置上评估。模型包括 LLaVA-1.5、InstructBLIP、Shikra、LLaVA-NeXT。Baselines 包括 Sampling、Greedy、DoLa、VCD、ICD 和 OPERA。结果显示 SID 在 object hallucination 和细粒度 hallucination 上整体优于多数 decoding baseline，同时基本保持通用多模态能力。效率上，SID 通常比 VCD / ICD 更快，远快于 OPERA，因为 OPERA 依赖 beam search 和 rollback，而 SID 只在早期层做 token-level selection。

---

## 与我研究的关系

SID 与我的 token-level / head-level / logit-level 视觉依赖研究高度相关。它本质上提供了一种内部视觉反事实：不是 real image vs blank image，而是 full visual evidence vs context-aware weak visual evidence。我的 VR 指标比较真实图像和空白图像 logits，而 SID 比较完整 vision tokens 和低重要性 vision tokens 的 logits。

可以将二者并列理解：

\[
VR(y_t)
=
l_{\mathrm{real}}(y_t)
-
l_{\mathrm{blank}}(y_t)
\]

\[
SIDGap(y_t)
=
l_{\mathrm{full}}(y_t)
-
l_{\mathrm{low}}(y_t)
\]

如果 hallucinated token 在 blank 分支和 low-vision 分支中都保持高 logit，说明它更可能来自语言先验；如果 grounded token 只在 full-image 分支中高，说明它更依赖视觉证据。

---

## 是否适合作为 baseline

SID 很适合作为后续 baseline 或 comparison method，尤其适合低算力研究。它不需要训练、不需要 object detector、不需要外部 LLM evaluator 参与生成，只需要能访问 decoder attention 和中间层输出。它比 M3ID 更贴近 attention/token 层面的机制分析，也比 OPERA 更容易和我的 head-level 分析结合。

但需要注意三点风险：

1. attention score 是否真的等价于 visual importance 仍需验证；
2. 论文对 heads 做平均，可能掩盖关键 head 的行为差异；
3. layer index 和保留比例有经验性，不同模型可能需要重新调参。

---

## 可做的 follow-up experiment

### 1. Blank image vs SID low-vision branch

比较三种反事实分支：blank image、noisy image、least-important vision tokens。记录 hallucinated object token 与 grounded object token 的 logit gap、rank shift 和 top-k 变化。如果 SID 分支更容易放大共现型幻觉，而 blank image 更像纯语言先验，就能说明内部视觉反事实比空白图像更适合分析 token-level hallucination。

### 2. Head-level SID

不要对 heads 求平均，而是逐 head 计算：

\[
Score_i^{(h)}(v_j)
=
A_i^{(h)}[-1, v_j]
\]

然后分别构造 head-specific low-vision branch，观察哪些 heads 的 low-token pruning 最容易诱发 hallucination token logit 上升。这可以直接连接我的 head-level visual dependence 分析。

### 3. Hallucinated token vs grounded token 的 SID gap

对生成 caption 中的 object tokens 进行分类：grounded object vs hallucinated object。比较：

\[
SIDGap(y_t)
=
l_{\mathrm{full}}(y_t)
-
l_{\mathrm{low}}(y_t)
\]

预期 grounded tokens 的 SIDGap 更大，因为它们更依赖完整视觉证据；hallucinated tokens 的 SIDGap 更小，甚至在 \(l_{\mathrm{low}}\) 中也很高，说明它们主要来自语言先验或上下文共现。

---

## 总结

SID 的核心贡献不是简单提出一个 decoding trick，而是提供了一个值得借鉴的内部反事实框架。它用模型自身 attention 找到当前上下文下不重要的视觉 tokens，构造一个“弱视觉但上下文相关”的 hallucination branch，再通过 logits subtraction 抑制这些 hallucination-prone tokens。对我的研究来说，SID 最有价值的地方在于：它把 hallucination 缓解、attention-based visual importance、token-level logits contrast 和内部反事实实验连接到了一起，是后续 baseline、related work 和实验设计的重要参考。

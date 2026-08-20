---
title: 资源库
description: 论文来源、评测资产、阅读产物与公开成果的独立目录
---

# 资源库

资源库只回答“有哪些可复用资产、成熟度如何、从哪里进入”，不承担跨论文机制结论。机制归纳位于[研究版图](../research-map.md)与各方向页，完整论文分析位于 [Deep Paper Notes](../papers/index.md)。这种边界避免方法列表、专题综述和评测说明互相复制。

<div class="atlas-grid">
  <a class="atlas-card" href="methods/"><span class="index">15 NOTES</span><h3>方法论文目录</h3><p>按干预层级连接全部已精读论文，不重复正文。</p></a>
  <a class="atlas-card" href="surveys/"><span class="index">SURVEY</span><h3>综述来源目录</h3><p>登记可核验综述来源；综合判断另在 Surveys 发布。</p></a>
  <a class="atlas-card" href="benchmarks/"><span class="index">EVAL</span><h3>Benchmark / Metric</h3><p>评测对象、协议、指标方向与最低审计项。</p></a>
  <a class="atlas-card" href="datasets/"><span class="index">DATA</span><h3>Dataset</h3><p>区分训练、检测、反事实和评测数据角色。</p></a>
</div>

## 完整性快照

| 检查项 | 当前结果 | 维护方式 |
|---|---:|---|
| 已登记 Deep Paper Notes | 15 | 由论文 front matter 生成总索引 |
| 有对应官方方法图/官方方法页裁图 | 15 / 15 | `validate_paper_notes.py` 强制检查元数据、图块与文件 |
| 本轮“待整理”方法论文 | 0 / 4 | 已全部迁移为 Deep Paper Note |
| 仍待判断的相邻工作 | 1 | 保留在[待读队列](reading-queue.md)，不混入方法目录 |

## 页面职责

| 页面 | 只负责 | 不负责 |
|---|---|---|
| 方法论文目录 | 按层级列出已精读论文 | 重复论文方法与实验正文 |
| 综述来源目录 | 登记综述来源和核对状态 | 发布未经综合的观点 |
| Surveys | 跨论文证据、冲突与开放问题 | 充当论文清单 |
| Benchmark / Dataset | 评测资产定义与使用风险 | 把使用该 benchmark 的论文全部复制一遍 |
| Reading Notes | 解释公开阅读产物的成熟度 | 收录私有批注或实验日志 |
| Published Research | 已公开成果与稳定链接 | 未投稿 hypothesis 或内部结果 |

## 状态约定

| 状态 | 含义 |
|---|---|
| 待读 | 仅登记来源，尚未形成结构化判断 |
| 速览 | 已提取核心问题和方法，但实验细节未完全核对 |
| 已精读 | 已覆盖方法、实验、局限、baseline 与研究启发 |
| 待复现 | 已精读并进入实现/实验队列 |

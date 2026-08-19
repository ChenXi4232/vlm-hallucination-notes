---
title: 公开 / 私有发布边界
description: 双仓库内容分流与发布前检查规则
---

# 公开 / 私有发布边界

公开仓库是研究知识索引层，私有仓库是研究执行层。**没有加入导航的公开仓库文件仍然是公开的。**

| 内容 | Public Notes | Private Lab |
|---|:---:|:---:|
| Deep Paper Note 与公开来源 | ✓ | 可引用 ID |
| Survey / Method Taxonomy | ✓ | 草稿先留私有 |
| Benchmark / Dataset 说明 | ✓ | 私有划分与标注可留存 |
| 清洗后的实验发现 | 发布后可选 | ✓ |
| 原始日志、命令、checkpoint | ✗ | ✓ |
| 未成熟 idea / hypothesis | ✗ | ✓ |
| Codex task 与内部计划 | ✗ | ✓ |
| 未发表方法与结果 | ✗ | ✓ |

## 关联方式

公开页面只记录不可反推私有内容的稳定编号：

```yaml
paper_id: allpath-2025
evidence_refs:
  - EXP-HEAD-017
  - EXP-RECALL-006
```

## 发布前检查

- [ ] 所有结论可回溯到公开论文或已公开成果。
- [ ] 已移除服务器路径、账号、token、日志和原始输出。
- [ ] 没有泄露未发表方法、超参数或内部结果。
- [ ] mitigation 同时报告 recall、长度、重复和质量变化。
- [ ] 已运行 `python scripts/check_public_boundary.py`。
- [ ] 已运行 `mkdocs build --strict` 与 HTML 校验。

#!/usr/bin/env python3
"""Build deterministic Markdown indexes from Deep Paper Note front matter."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "docs" / "papers"


def read_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        raise SystemExit(f"Missing YAML front matter: {path.relative_to(ROOT)}")
    data = yaml.safe_load(match.group(1)) or {}
    required = {
        "title",
        "year",
        "venue",
        "resource_type",
        "direction",
        "status",
        "added_at",
        "tags",
    }
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit(f"Missing {', '.join(missing)}: {path.relative_to(ROOT)}")
    try:
        data["added_at"] = date.fromisoformat(str(data["added_at"])).isoformat()
    except ValueError as error:
        raise SystemExit(
            f"Invalid added_at (expected YYYY-MM-DD): {path.relative_to(ROOT)}"
        ) from error
    data["path"] = path
    return data


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def link(card: dict) -> str:
    return f"[{esc(card['title'])}]({card['path'].name})"


def main() -> None:
    cards = sorted(
        (read_card(path) for path in PAPERS.glob("*.md") if path.name != "index.md"),
        key=lambda item: (
            -date.fromisoformat(str(item["added_at"])).toordinal(),
            -int(item["year"]),
            str(item["title"]).lower(),
        ),
    )
    if not cards:
        raise SystemExit("No Paper Notes found")

    directions = Counter(str(card["direction"]) for card in cards)
    resources = Counter(str(card["resource_type"]) for card in cards)
    venues = Counter(str(card["venue"]) for card in cards)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for card in cards:
        grouped[str(card["direction"])].append(card)

    lines = [
        "---",
        "title: 论文总索引",
        "description: 由 Deep Paper Note front matter 自动生成",
        "---",
        "",
        "# 论文总索引",
        "",
        "此页由 `scripts/build_indexes.py` 根据 Deep Paper Note front matter 自动生成。分类是多维元数据，不要求一篇论文只能属于一个文件夹。",
        "",
        '<div class="stat-grid">',
        f'<div class="stat-card"><strong>{len(cards)}</strong><span>Deep Paper Notes</span></div>',
        f'<div class="stat-card"><strong>{len(directions)}</strong><span>研究方向</span></div>',
        f'<div class="stat-card"><strong>{len(venues)}</strong><span>来源类型</span></div>',
        f'<div class="stat-card"><strong>{sum(card["status"] == "已精读" for card in cards)}</strong><span>已精读</span></div>',
        "</div>",
        "",
        '<div class="paper-index-toolbar" data-paper-index-toolbar>',
        '  <label for="paper-index-sort">排序方式</label>',
        '  <select id="paper-index-sort" aria-label="论文排序方式">',
        '    <option value="added-desc">收录时间：最新优先</option>',
        '    <option value="added-asc">收录时间：最早优先</option>',
        '    <option value="year-desc">论文年份：新到旧</option>',
        '    <option value="title-asc">标题：A–Z</option>',
        "  </select>",
        f'  <span class="paper-sort-status" aria-live="polite">共 {len(cards)} 篇</span>',
        "</div>",
        "",
        '<div id="paper-index-table" markdown="1">',
        "",
        "| 论文 | 收录时间 | 年份 / 来源 | 研究方向 | 资源类型 | 状态 |",
        "|---|---:|---:|---|---|---|",
    ]
    for card in cards:
        lines.append(
            f"| {link(card)} | {esc(card['added_at'])} | {esc(card['year'])} · {esc(card['venue'])} | "
            f"{esc(card['direction'])} | {esc(card['resource_type'])} | {esc(card['status'])} |"
        )

    lines.extend(["", "</div>", "", "## 按研究方向", ""])
    for direction in sorted(grouped):
        lines.extend([f"### {direction}", ""])
        lines.extend(f"- {link(card)}" for card in grouped[direction])
        lines.append("")

    lines.extend(["## 当前覆盖", "", "### 资源类型", ""])
    lines.extend(f"- **{name}**：{count}" for name, count in resources.most_common())
    lines.extend(["", "### 论文来源", ""])
    lines.extend(f"- **{name}**：{count}" for name, count in venues.most_common())
    lines.append("")

    (PAPERS / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated index for {len(cards)} Deep Paper Notes")


if __name__ == "__main__":
    main()

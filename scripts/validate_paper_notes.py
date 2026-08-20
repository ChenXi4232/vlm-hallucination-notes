#!/usr/bin/env python3
"""Validate that published paper pages follow the deep-note contract."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "docs" / "papers"
METHOD_CATALOG = ROOT / "docs" / "library" / "methods.md"
MKDOCS_CONFIG = ROOT / "mkdocs.yml"
REQUIRED_META = {
    "title",
    "description",
    "authors",
    "venue",
    "year",
    "resource_type",
    "direction",
    "hallucination_type",
    "method_level",
    "training",
    "status",
    "source_status",
    "review_state",
    "paper_url",
    "overview_figure",
    "overview_figure_source",
    "tags",
}
REQUIRED_SECTIONS = [
    "论文速览",
    "研究背景",
    "方法详解",
    "实验设计",
    "亮点与贡献",
    "局限",
    "与我的研究关系",
    "可执行的后续实验",
    "复现清单",
    "综合评分",
    "来源边界",
]


def front_matter(text: str, path: Path) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        raise ValueError(f"missing YAML front matter: {path}")
    return yaml.safe_load(match.group(1)) or {}


def main() -> None:
    errors: list[str] = []
    paper_paths = sorted(path for path in PAPERS.glob("*.md") if path.name != "index.md")
    method_catalog = METHOD_CATALOG.read_text(encoding="utf-8")
    nav_config = MKDOCS_CONFIG.read_text(encoding="utf-8")
    for path in paper_paths:
        text = path.read_text(encoding="utf-8")
        try:
            meta = front_matter(text, path)
        except ValueError as error:
            errors.append(str(error))
            continue
        missing_meta = sorted(REQUIRED_META - set(meta))
        if missing_meta:
            errors.append(f"{path.name}: missing metadata {', '.join(missing_meta)}")
        missing_sections = [name for name in REQUIRED_SECTIONS if name not in text]
        if missing_sections:
            errors.append(f"{path.name}: missing sections {', '.join(missing_sections)}")
        if "paper-tldr" not in text:
            errors.append(f"{path.name}: missing one-line summary block")
        if "paper-figure" not in text or "官方方法概览图" not in text:
            errors.append(f"{path.name}: missing official method overview figure block")
        figure_path = meta.get("overview_figure")
        if figure_path:
            resolved_figure = (path.parent / str(figure_path)).resolve()
            try:
                resolved_figure.relative_to(ROOT / "docs")
            except ValueError:
                errors.append(f"{path.name}: overview figure points outside docs: {figure_path}")
            else:
                if not resolved_figure.is_file():
                    errors.append(f"{path.name}: overview figure not found: {figure_path}")
        if len(text) < 4500:
            errors.append(f"{path.name}: body is too short for a Deep Paper Note")
        if f"../papers/{path.name}" not in method_catalog:
            errors.append(f"{path.name}: missing from resource method catalog")
        if f"papers/{path.name}" not in nav_config:
            errors.append(f"{path.name}: missing from Paper Notes navigation")
    if errors:
        raise SystemExit("Deep Paper Note validation failed:\n- " + "\n- ".join(errors))
    print("Deep Paper Note validation passed")


if __name__ == "__main__":
    main()

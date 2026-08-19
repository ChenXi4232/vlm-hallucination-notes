#!/usr/bin/env python3
"""Verify that generated HTML pages have titles and resolvable local links."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SITE_PREFIX = "/vlm-hallucination-notes"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def target_for(site: Path, page: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:", "javascript:")):
        return None
    raw = unquote(parsed.path)
    if not raw:
        return None
    if raw == SITE_PREFIX or raw.startswith(f"{SITE_PREFIX}/"):
        raw = raw[len(SITE_PREFIX) :] or "/"
    target = site / raw.lstrip("/") if raw.startswith("/") else page.parent / raw
    if raw.endswith("/"):
        target /= "index.html"
    elif not target.suffix:
        target /= "index.html"
    return target.resolve()


def main() -> None:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    errors: list[str] = []
    pages = sorted(site.rglob("*.html"))
    if not pages:
        raise SystemExit("No HTML files generated")
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if not parser.title.strip():
            errors.append(f"Missing title: {page.relative_to(site)}")
        for href in parser.links:
            target = target_for(site, page, href)
            if target is not None and site not in target.parents and target != site:
                errors.append(f"Escapes site root: {page.relative_to(site)} -> {href}")
            elif target is not None and not target.exists():
                errors.append(f"Broken local link: {page.relative_to(site)} -> {href}")
    if errors:
        raise SystemExit("\n".join(errors[:50]))
    print(f"Verified {len(pages)} HTML pages")


if __name__ == "__main__":
    main()

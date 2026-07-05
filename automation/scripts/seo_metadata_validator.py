#!/usr/bin/env python3
"""Validate draft SEO metadata without publishing or modifying content."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEFAULT_DIRS = [
    Path("content/drafts"),
    Path("content/pending-review"),
    Path("03_CONTENT/_drafts"),
]

REQUIRED_FIELDS = [
    "generated-by-ai",
    "status",
    "content-type",
    "target-keyword",
    "seo-title",
    "meta-description",
    "privacy-reviewed",
]


def read_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fields = read_frontmatter(text)
    issues: list[str] = []
    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            issues.append(f"missing frontmatter field: {field}")
    title = fields.get("seo-title", "")
    meta = fields.get("meta-description", "")
    if title and len(title) > 70:
        issues.append(f"seo-title is long: {len(title)} chars")
    if meta and not (80 <= len(meta) <= 180):
        issues.append(f"meta-description length is {len(meta)} chars")
    h1_count = len(re.findall(r"^#\s+", text, flags=re.MULTILINE))
    if h1_count != 1:
        issues.append(f"expected exactly one H1, found {h1_count}")
    if "status: published" in text.lower():
        issues.append("draft file must not be marked published")
    return issues


def main(argv: list[str]) -> int:
    targets = [Path(arg) for arg in argv[1:]] or DEFAULT_DIRS
    files: list[Path] = []
    for target in targets:
        if target.is_file() and target.suffix.lower() == ".md":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.glob("*.md")))

    if not files:
        print("No Markdown draft files found.")
        return 0

    failed = False
    for path in files:
        issues = validate_file(path)
        if issues:
            failed = True
            print(f"FAIL {path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"OK   {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

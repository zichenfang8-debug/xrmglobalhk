#!/usr/bin/env python3
"""Generate a review checklist for a draft blog/article file."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path


CHECKS = [
    "SEO title and meta description reviewed",
    "Target keyword appears in filename or H1",
    "Only one H1 is present",
    "Confidential names and private project details removed",
    "Claims marked Needs verification where uncertain",
    "Internal links reviewed",
    "RFQ call-to-action reviewed",
    "Draft remains in draft or pending-review path",
    "Human approval required before publication",
]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: generate_blog_review_checklist.py <draft-markdown-file>")
        return 2

    draft = Path(argv[1])
    if not draft.exists():
        print(f"Draft not found: {draft}")
        return 1

    date = dt.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path("automation/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{date}-{draft.stem}-review-checklist.md"

    lines = [
        "# Blog Draft Review Checklist",
        "",
        f"- Draft: `{draft}`",
        f"- Generated: {date}",
        "- Status: pending-review",
        "",
        "## Checks",
        "",
    ]
    lines.extend([f"- [ ] {item}" for item in CHECKS])
    lines.extend([
        "",
        "## Reviewer Notes",
        "",
        "- ",
        "",
    ])

    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

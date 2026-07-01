#!/usr/bin/env python3
"""Generate a review checklist Markdown file for a nightly AI run."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


CHECKLIST = """---
generated-by-ai: true
status: pending-review
report-type: review-checklist
run-date: {run_date}
---

# AI Nightly Review Checklist - {run_date}

- [ ] Confirm all outputs are in `content/drafts/`, `content/pending-review/`, or `data/`.
- [ ] Confirm no published website files were changed automatically.
- [ ] Confirm no old pages, content, or images were deleted.
- [ ] Confirm website drafts do not contain real hotel project names.
- [ ] Confirm supplier-facing drafts do not contain customer or hotel party information.
- [ ] Confirm no Wang-ge information appears in external drafts.
- [ ] Confirm no XRM company name, logo, contact information, or company seal appears in external drafts.
- [ ] Confirm supplier database updates have source evidence.
- [ ] Confirm hotel procurement updates have source evidence.
- [ ] Confirm website article drafts are factually supported.
- [ ] Confirm social media drafts are public-safe.
- [ ] Decide: approve, edit, reject, or defer each generated item.
- [ ] Merge PR only after human approval.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AI nightly review checklist.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Run date in YYYY-MM-DD format.")
    parser.add_argument(
        "--output-dir",
        default="automation/reports",
        help="Directory for the checklist Markdown file.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.date}-review-checklist.md"
    output_path.write_text(CHECKLIST.format(run_date=args.date), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

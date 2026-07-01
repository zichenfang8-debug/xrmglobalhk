#!/usr/bin/env python3
"""Run a local dry-run of the Nightly AI Workflow using a test file.

This does not call Google Drive, OpenAI, GitHub, Cloudflare, SMTP, or n8n. It
creates the same kind of draft/report/checklist files so the repository side of
the workflow can be verified before external credentials are connected.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def classify(text: str) -> dict:
    lower = text.lower()
    categories = []
    if "supplier" in lower:
        categories.append("supplier_profile")
    if "hotel" in lower or "ff&e" in lower or "os&e" in lower:
        categories.append("hotel_project")
    if "website" in lower:
        categories.append("website_content_material")
    if not categories:
        categories.append("other")
    return {
        "primary_category": categories[0],
        "secondary_categories": categories[1:],
        "confidence": 0.78,
        "privacy_risk": "low",
    }


def front_matter(run_date: str, content_type: str) -> str:
    return (
        "---\n"
        "generated-by-ai: true\n"
        "status: pending-review\n"
        f"run-date: {run_date}\n"
        f"content-type: {content_type}\n"
        "privacy-reviewed: required\n"
        "---\n\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create local nightly workflow test outputs.")
    parser.add_argument("--source", default="automation/test-files/nightly-test-source.md")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    run_date = args.date
    source_path = Path(args.source)
    source = read_source(source_path)
    classification = classify(source)

    Path("content/drafts").mkdir(parents=True, exist_ok=True)
    Path("content/pending-review").mkdir(parents=True, exist_ok=True)
    Path("data/suppliers").mkdir(parents=True, exist_ok=True)
    Path("data/projects").mkdir(parents=True, exist_ok=True)
    Path("data/knowledge-base").mkdir(parents=True, exist_ok=True)
    Path("automation/reports").mkdir(parents=True, exist_ok=True)

    supplier_update = {
        "generated_by_ai": True,
        "status": "pending-review",
        "supplier_updates": [
            {
                "supplier_id": f"SUP-{run_date.replace('-', '')}-TEST",
                "public_display_name": "Public-Safe Supplier A",
                "category": ["hotel FF&E", "hotel OS&E"],
                "lead_time": "35-45 days after sample approval",
                "privacy_flags": [],
                "next_actions": ["Request updated MOQ and packaging details"],
            }
        ],
    }

    project_update = {
        "generated_by_ai": True,
        "status": "pending-review",
        "hotel_procurement_updates": [
            {
                "project_placeholder": "Southeast Asia Hotel Project A",
                "classification": "FF&E|OS&E",
                "item_name": "Guestroom furniture and operating supplies",
                "open_questions": ["Confirm MOQ", "Confirm packaging details"],
                "privacy_flags": [],
            }
        ],
    }

    report = front_matter(run_date, "ai-nightly-work-report") + f"""# AI Nightly Work Report - {run_date}

## Run Summary

- Source: `{source_path}`
- Classification: `{classification['primary_category']}`
- Privacy risk: `{classification['privacy_risk']}`
- Publication: draft only

## Generated Outputs

- `content/drafts/{run_date}-website-draft.md`
- `content/pending-review/{run_date}-nightly-output.md`
- `data/suppliers/{run_date}-supplier-updates.json`
- `data/projects/{run_date}-project-updates.json`

## Review Checklist

- [ ] No sensitive hotel/customer/internal details
- [ ] No automatic publication
- [ ] Human approval required before merge
"""

    website_draft = front_matter(run_date, "website-article") + """# How a China Procurement Partner Supports Southeast Asia Hotel Procurement

A China procurement partner can help hotel teams coordinate supplier research, quotation comparison, sample follow-up, production tracking, and export documentation across FF&E and OS&E categories.

For Southeast Asia hospitality projects, the value is not only finding factories. The practical work is turning fragmented supplier information into a reviewable procurement workflow with clear specifications, lead times, quality notes, and next actions.

## Review Checklist

- [ ] Public-safe wording
- [ ] No real project names
- [ ] No customer information
- [ ] Human approval before publication
"""

    pending = front_matter(run_date, "nightly-output") + "# Nightly Output\n\n```json\n" + json.dumps(
        {
            "classification": classification,
            "supplier_update": supplier_update,
            "project_update": project_update,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n```\n"

    Path(f"automation/reports/{run_date}-ai-nightly-report.md").write_text(report, encoding="utf-8")
    Path(f"content/drafts/{run_date}-website-draft.md").write_text(website_draft, encoding="utf-8")
    Path(f"content/pending-review/{run_date}-nightly-output.md").write_text(pending, encoding="utf-8")
    Path(f"data/suppliers/{run_date}-supplier-updates.json").write_text(
        json.dumps(supplier_update, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    Path(f"data/projects/{run_date}-project-updates.json").write_text(
        json.dumps(project_update, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "ok": True,
                "run_date": run_date,
                "outputs": [
                    f"automation/reports/{run_date}-ai-nightly-report.md",
                    f"content/drafts/{run_date}-website-draft.md",
                    f"content/pending-review/{run_date}-nightly-output.md",
                    f"data/suppliers/{run_date}-supplier-updates.json",
                    f"data/projects/{run_date}-project-updates.json",
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

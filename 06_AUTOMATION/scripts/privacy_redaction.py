#!/usr/bin/env python3
"""Local privacy scanner for generated draft files.

This script is intentionally conservative. It flags likely sensitive terms before
drafts are pushed or reviewed. It does not replace AI redaction or human review.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_PATTERNS = {
    "xrm_name": r"\bXRM\b|XRM GLOBAL TRADE LIMITED",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"(?<![A-Z0-9-])(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{10,12}(?![A-Z0-9-])",
    "seal": r"company seal|chop|印章|公章",
    "hotel": r"hotel project real name|酒店真实名称|业主方|酒店方",
    "wang_ge": r"王哥",
}


def scan_text(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for label, pattern in DEFAULT_PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            start = max(match.start() - 30, 0)
            end = min(match.end() + 30, len(text))
            findings.append(
                {
                    "type": label,
                    "match": match.group(0),
                    "context": text[start:end].replace("\n", " "),
                }
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan generated drafts for sensitive information.")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    files: list[Path] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
        elif path.is_file():
            files.append(path)

    results = []
    for file_path in files:
        if file_path.suffix.lower() not in {".md", ".txt", ".json", ".csv"}:
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        findings = scan_text(text)
        if findings:
            results.append({"file": str(file_path), "findings": findings})

    if args.json:
        print(json.dumps({"privacy_risk": "high" if results else "low", "results": results}, indent=2))
    else:
        if not results:
            print("No configured sensitive patterns detected.")
        for result in results:
            print(f"\n{result['file']}")
            for finding in result["findings"]:
                print(f"- {finding['type']}: {finding['match']} | {finding['context']}")

    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())

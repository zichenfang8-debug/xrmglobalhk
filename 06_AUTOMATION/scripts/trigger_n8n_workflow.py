#!/usr/bin/env python3
"""Trigger or inspect the imported n8n Nightly AI Workflow."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request


def request_json(url: str, api_key: str, method: str = "GET", payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        headers={"X-N8N-API-KEY": api_key, "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return {"status": response.status, "body": json.loads(raw) if raw else {}}
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect n8n workflow by API.")
    parser.add_argument("--workflow-id", default=os.environ.get("N8N_WORKFLOW_ID", ""))
    parser.add_argument("--base-url", default=os.environ.get("N8N_BASE_URL", "").rstrip("/"))
    parser.add_argument("--api-key", default=os.environ.get("N8N_API_KEY", ""))
    args = parser.parse_args()

    if not args.base_url or not args.api_key:
        raise SystemExit("Set N8N_BASE_URL and N8N_API_KEY.")

    if args.workflow_id:
        result = request_json(f"{args.base_url}/api/v1/workflows/{args.workflow_id}", args.api_key)
    else:
        result = request_json(f"{args.base_url}/api/v1/workflows", args.api_key)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

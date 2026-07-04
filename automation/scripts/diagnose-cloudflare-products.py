#!/usr/bin/env python3
"""Query Cloudflare product surfaces that can reference n8n.xrmglobalhk.com."""

from __future__ import annotations

import importlib.util
import json
import urllib.parse
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
FIX_SCRIPT = WORKSPACE / "automation/scripts/fix-cloudflare-n8n-dns.py"
HOSTNAME = "n8n.xrmglobalhk.com"


def load_fix_module():
    spec = importlib.util.spec_from_file_location("fix_cloudflare_n8n_dns", FIX_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {FIX_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fix = load_fix_module()


def maybe_get(label: str, path: str) -> dict:
    try:
        payload = fix.cf_request("GET", path)
        return {
            "label": label,
            "ok": True,
            "matched_n8n": HOSTNAME in json.dumps(payload, ensure_ascii=False),
            "result": payload.get("result"),
            "result_info": payload.get("result_info"),
        }
    except Exception as exc:
        return {"label": label, "ok": False, "error": str(exc)}


def main() -> int:
    zone_id = fix.get_zone_id()
    zone = fix.cf_request("GET", f"/zones/{zone_id}")["result"]
    account_id = zone["account"]["id"]

    checks = [
        ("workers-routes-zone", f"/zones/{zone_id}/workers/routes"),
        ("zone-rulesets", f"/zones/{zone_id}/rulesets"),
        ("custom-hostnames-zone", f"/zones/{zone_id}/custom_hostnames?{urllib.parse.urlencode({'hostname': HOSTNAME})}"),
        ("pages-projects-account", f"/accounts/{account_id}/pages/projects"),
        ("cloudflare-tunnels-account", f"/accounts/{account_id}/cfd_tunnel?is_deleted=false"),
        ("access-apps-account", f"/accounts/{account_id}/access/apps"),
        ("account-rulesets", f"/accounts/{account_id}/rulesets"),
    ]

    results = [maybe_get(label, path) for label, path in checks]
    print(json.dumps(
        {
            "zone_id": zone_id,
            "account_id": account_id,
            "hostname": HOSTNAME,
            "results": results,
        },
        indent=2,
        ensure_ascii=False,
    ))

    matched = [item for item in results if item.get("ok") and item.get("matched_n8n")]
    if matched:
        print("PRODUCT_REFERENCE_FOUND")
        return 2

    denied = [item for item in results if not item.get("ok") and "403" in item.get("error", "")]
    if denied:
        print("PRODUCT_CHECKS_BLOCKED_BY_TOKEN_SCOPE")
        return 3

    print("NO_PRODUCT_REFERENCE_FOUND")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

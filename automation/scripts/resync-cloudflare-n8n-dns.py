#!/usr/bin/env python3
"""Force-resync Cloudflare DNS record for n8n.xrmglobalhk.com.

This script uses the visible DNS record API only. It does not print secrets.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
FIX_SCRIPT = WORKSPACE / "automation/scripts/fix-cloudflare-n8n-dns.py"
HOSTNAME = "n8n.xrmglobalhk.com"
RECORD_NAME = "n8n"
GOOD_IP = "178.105.167.227"


def load_fix_module():
    spec = importlib.util.spec_from_file_location("fix_cloudflare_n8n_dns", FIX_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {FIX_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fix = load_fix_module()


def get_n8n_record(zone_id: str) -> dict | None:
    records = fix.list_all_records(zone_id)
    matches = [
        record
        for record in records
        if record.get("name") == HOSTNAME
        and record.get("type") == "A"
    ]
    if not matches:
        return None
    return matches[0]


def put_record(zone_id: str, record_id: str, proxied: bool, comment: str) -> dict:
    payload = {
        "type": "A",
        "name": RECORD_NAME,
        "content": GOOD_IP,
        "ttl": 1,
        "proxied": proxied,
        "comment": comment,
    }
    return fix.cf_request("PUT", f"/zones/{zone_id}/dns_records/{record_id}", payload)["result"]


def main() -> int:
    zone_id = fix.get_zone_id()
    record = get_n8n_record(zone_id)
    if record is None:
        print("No visible n8n A record found; creating correct DNS-only record.")
        record = fix.create_good_record(zone_id)

    print(
        "Visible record before resync: "
        f"id={record.get('id')} name={record.get('name')} content={record.get('content')} "
        f"proxied={record.get('proxied')} ttl={record.get('ttl')}"
    )

    print("Resync step 1/3: temporarily toggling proxied=true through Cloudflare API.")
    updated = put_record(zone_id, record["id"], True, f"temporary resync toggle {int(time.time())}")
    print(
        "Updated temporary record: "
        f"id={updated.get('id')} content={updated.get('content')} proxied={updated.get('proxied')}"
    )
    time.sleep(10)

    print("Resync step 2/3: restoring DNS-only proxied=false.")
    restored = put_record(zone_id, record["id"], False, f"n8n HTTPS endpoint DNS-only resync {int(time.time())}")
    print(
        "Restored record: "
        f"id={restored.get('id')} content={restored.get('content')} proxied={restored.get('proxied')}"
    )

    print("Resync step 3/3: verifying DNS for up to 180 seconds.")
    deadline = time.time() + 180
    last = {}
    while time.time() < deadline:
        last = fix.verify_dns()
        if all(values == [GOOD_IP] for values in last.values()):
            break
        time.sleep(5)
    print(json.dumps(last, indent=2, ensure_ascii=False))
    if all(values == [GOOD_IP] for values in last.values()):
        print("DNS FIX SUCCESS")
        return 0

    print("RESYNC FAILED: API-visible record is correct, but DNS authority still serves another value.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

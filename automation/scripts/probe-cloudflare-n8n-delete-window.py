#!/usr/bin/env python3
"""Probe whether Cloudflare authoritative DNS keeps returning stale n8n A data.

This script temporarily deletes API-visible n8n DNS records, checks authoritative
DNS while no visible n8n record exists, and then recreates the correct DNS-only
A record in a finally block.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import time


WORKSPACE = pathlib.Path(__file__).resolve().parents[2]
FIX_SCRIPT = WORKSPACE / "automation/scripts/fix-cloudflare-n8n-dns.py"
HOSTNAME = "n8n.xrmglobalhk.com"
TARGET_IP = "178.105.167.227"


def load_fix_module():
    spec = importlib.util.spec_from_file_location("fix_cloudflare_n8n_dns", FIX_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {FIX_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    fix = load_fix_module()
    fix.token()
    zone_id = fix.get_zone_id()

    records = fix.list_all_records(zone_id)
    n8n_records = [record for record in records if fix.is_n8n_record(record)]

    print(f"Zone ID: {zone_id}")
    print(f"API-visible n8n records before probe: {len(n8n_records)}")
    for record in n8n_records:
        print(
            "Visible before delete: "
            f"id={record.get('id')} type={record.get('type')} "
            f"name={record.get('name')} content={record.get('content')} "
            f"proxied={record.get('proxied')} ttl={record.get('ttl')}"
        )

    try:
        for record in n8n_records:
            fix.delete_record(zone_id, record)
            print(f"Deleted visible record: {record['id']}")

        time.sleep(20)
        after_delete_records = fix.list_all_records(zone_id)
        after_delete_n8n = [record for record in after_delete_records if fix.is_n8n_record(record)]
        print(f"API-visible n8n records after delete: {len(after_delete_n8n)}")

        dig_after_delete = fix.verify_dns()
        print("Authoritative/public DNS while API-visible n8n record is absent:")
        print(json.dumps(dig_after_delete, indent=2, ensure_ascii=False))

        if any("172.29.0.127" in values for values in dig_after_delete.values()):
            print("PROBE_RESULT: STALE_OR_SHADOW_RECORD_CONFIRMED")
            return 4

        print("PROBE_RESULT: NO_STALE_RECORD_AFTER_DELETE")
        return 0
    finally:
        current_records = fix.list_all_records(zone_id)
        current_n8n = [record for record in current_records if fix.is_n8n_record(record)]
        for record in current_n8n:
            fix.delete_record(zone_id, record)
            print(f"Cleanup delete before restore: {record['id']}")
        restored = fix.create_good_record(zone_id)
        print(
            "Restored correct record: "
            f"id={restored.get('id')} type={restored.get('type')} "
            f"name={restored.get('name')} content={restored.get('content')} "
            f"proxied={restored.get('proxied')} ttl={restored.get('ttl')}"
        )
        time.sleep(10)
        final_dig = fix.verify_dns()
        print("DNS after restore:")
        print(json.dumps(final_dig, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())

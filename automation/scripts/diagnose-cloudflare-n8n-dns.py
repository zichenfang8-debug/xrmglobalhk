#!/usr/bin/env python3
"""Diagnose Cloudflare DNS backend inconsistency for n8n.xrmglobalhk.com.

Loads CF_API_TOKEN from the same locations as fix-cloudflare-n8n-dns.py.
Does not print secrets.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import urllib.parse
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
FIX_SCRIPT = WORKSPACE / "automation/scripts/fix-cloudflare-n8n-dns.py"
HOSTNAME = "n8n.xrmglobalhk.com"
WILDCARD = "*.xrmglobalhk.com"
RANDOM_HOSTS = [
    "random-shadow-probe-20260704.xrmglobalhk.com",
    "another-random-shadow-20260704.xrmglobalhk.com",
]
GOOD_IP = "178.105.167.227"
BAD_IP = "172.29.0.127"


def load_fix_module():
    spec = importlib.util.spec_from_file_location("fix_cloudflare_n8n_dns", FIX_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {FIX_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fix = load_fix_module()


def dig(server: str, name: str) -> list[str]:
    result = subprocess.run(
        ["dig", f"@{server}", "+short", name, "A"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    if result.returncode != 0:
        return [f"ERROR: {result.stderr.strip()}"]
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def api_get(path: str) -> dict:
    return fix.cf_request("GET", path)


def maybe_get(label: str, path: str) -> dict:
    try:
        payload = api_get(path)
        return {
            "label": label,
            "ok": True,
            "result": payload.get("result"),
            "result_info": payload.get("result_info"),
        }
    except Exception as exc:
        return {"label": label, "ok": False, "error": str(exc)}


def main() -> int:
    zone_id = fix.get_zone_id()
    print(f"Zone ID: {zone_id}")

    zone = maybe_get("zone-details", f"/zones/{zone_id}")
    print(json.dumps(zone, indent=2, ensure_ascii=False))

    params_all = urllib.parse.urlencode({"per_page": 100, "page": 1})
    all_records = maybe_get("dns-records-page-1", f"/zones/{zone_id}/dns_records?{params_all}")
    print(json.dumps(all_records, indent=2, ensure_ascii=False))

    params_name = urllib.parse.urlencode({"name": HOSTNAME, "per_page": 100})
    name_records = maybe_get("dns-records-exact-hostname", f"/zones/{zone_id}/dns_records?{params_name}")
    print(json.dumps(name_records, indent=2, ensure_ascii=False))

    params_search = urllib.parse.urlencode({"search": "n8n", "per_page": 100})
    search_records = maybe_get("dns-records-search-n8n", f"/zones/{zone_id}/dns_records?{params_search}")
    print(json.dumps(search_records, indent=2, ensure_ascii=False))

    params_wildcard = urllib.parse.urlencode({"name": WILDCARD, "per_page": 100})
    wildcard_records = maybe_get("dns-records-exact-wildcard", f"/zones/{zone_id}/dns_records?{params_wildcard}")
    print(json.dumps(wildcard_records, indent=2, ensure_ascii=False))

    params_search_wildcard = urllib.parse.urlencode({"search": "*", "per_page": 100})
    wildcard_search = maybe_get(
        "dns-records-search-wildcard",
        f"/zones/{zone_id}/dns_records?{params_search_wildcard}",
    )
    print(json.dumps(wildcard_search, indent=2, ensure_ascii=False))

    export_zone = maybe_get("dns-records-export-bind", f"/zones/{zone_id}/dns_records/export")
    print(json.dumps(export_zone, indent=2, ensure_ascii=False))

    dnssec = maybe_get("dnssec", f"/zones/{zone_id}/dnssec")
    print(json.dumps(dnssec, indent=2, ensure_ascii=False))

    settings = {}
    for setting in ["cname_flattening", "foundation_dns", "zone_mode", "development_mode"]:
        settings[setting] = maybe_get(f"setting-{setting}", f"/zones/{zone_id}/settings/{setting}")
    print(json.dumps({"label": "zone-settings", "items": settings}, indent=2, ensure_ascii=False))

    servers = ["mina.ns.cloudflare.com", "nicolas.ns.cloudflare.com", "1.1.1.1", "8.8.8.8"]
    dig_results = {server: dig(server, HOSTNAME) for server in servers}
    print(json.dumps({"label": "dig-results", "items": dig_results}, indent=2, ensure_ascii=False))

    wildcard_dig_results = {server: dig(server, WILDCARD) for server in servers}
    print(json.dumps({"label": "wildcard-dig-results", "items": wildcard_dig_results}, indent=2, ensure_ascii=False))

    random_dig_results = {
        host: {server: dig(server, host) for server in servers[:2]}
        for host in RANDOM_HOSTS
    }
    print(json.dumps({"label": "random-host-dig-results", "items": random_dig_results}, indent=2, ensure_ascii=False))

    api_has_good = False
    if name_records.get("ok"):
        api_has_good = any(
            rec.get("type") == "A"
            and rec.get("name") == HOSTNAME
            and rec.get("content") == GOOD_IP
            and rec.get("proxied") is False
            for rec in (name_records.get("result") or [])
        )

    auth_has_bad = any(values == [BAD_IP] for values in dig_results.values())
    auth_has_good = all(values == [GOOD_IP] for values in dig_results.values())
    api_has_wildcard = bool((wildcard_records.get("result") or []) if wildcard_records.get("ok") else [])
    auth_has_hidden_wildcard = any(
        any(value.startswith("172.29.0.") for value in values)
        for host_result in random_dig_results.values()
        for values in host_result.values()
    )

    if api_has_good and auth_has_good:
        print("DNS FIX SUCCESS")
        return 0

    if api_has_good and auth_has_bad:
        if auth_has_hidden_wildcard and not api_has_wildcard:
            print(
                "DIAGNOSIS: Cloudflare API/UI show no wildcard record, but Cloudflare "
                "authoritative nameservers answer random subdomains with private 172.29.0.x "
                "addresses. This confirms a hidden wildcard/backend DNS record in addition "
                "to the stale n8n host answer."
            )
            return 3
        print(
            "DIAGNOSIS: Cloudflare API shows the correct DNS-only A record, "
            "but Cloudflare authoritative/public resolvers still return 172.29.0.127. "
            "This is evidence of a Cloudflare backend shadow/stale/generated DNS record "
            "or propagation bug outside the visible DNS Records API."
        )
        return 2

    print("DIAGNOSIS: DNS is still inconsistent; review API and dig evidence above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

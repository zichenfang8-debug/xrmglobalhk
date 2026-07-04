#!/usr/bin/env python3
"""Fix n8n.xrmglobalhk.com DNS in Cloudflare.

Configuration:
  CF_API_TOKEN

The script loads CF_API_TOKEN from the first available source:
  1. .env
  2. .env.local
  3. .env.production
  4. process environment
  5. launchctl environment
  6. macOS Keychain

This script does not print the token. It only manages DNS records in the
specific zone discovered for xrmglobalhk.com.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    from dotenv import load_dotenv
except ImportError:  # Keep a small fallback so setup can still diagnose itself.
    load_dotenv = None


API = "https://api.cloudflare.com/client/v4"
ZONE_NAME = "xrmglobalhk.com"
HOSTNAME = "n8n.xrmglobalhk.com"
RECORD_NAME = "n8n"
BAD_IP = "172.29.0.127"
GOOD_IP = "178.105.167.227"


class CfError(RuntimeError):
    pass


def load_dotenv_files() -> None:
    candidates = [".env", ".env.local", ".env.production"]
    if load_dotenv is not None:
        for rel_path in candidates:
            if os.path.exists(rel_path):
                load_dotenv(rel_path, override=False)
        return

    for rel_path in candidates:
        if not os.path.exists(rel_path):
            continue
        try:
            for line in open(rel_path, "r", encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.replace("export ", "").strip()
                if key in os.environ:
                    continue
                value = value.strip()
                if (value.startswith("'") and value.endswith("'")) or (
                    value.startswith('"') and value.endswith('"')
                ):
                    value = value[1:-1]
                os.environ[key] = value
        except OSError:
            continue


def token() -> str:
    load_dotenv_files()
    value = os.environ.get("CF_API_TOKEN", "").strip()
    if not value:
        value = load_token_from_launchctl()
    if not value:
        value = load_token_from_keychain()
    if not value:
        raise CfError(
            "Missing CF_API_TOKEN. Checked .env, .env.local, .env.production, "
            "process environment, launchctl environment, and macOS Keychain service names. "
            "Install dependencies with `python3 -m pip install -r requirements.txt` for python-dotenv support."
        )
    return value


def token_state() -> dict:
    load_dotenv_files()
    env_files = [name for name in [".env", ".env.local", ".env.production"] if os.path.exists(name)]
    value = (
        os.environ.get("CF_API_TOKEN", "").strip()
        or load_token_from_launchctl()
        or load_token_from_keychain()
    )
    return {
        "env_files_found": env_files,
        "cf_api_token_present": bool(value),
        "cf_api_token_empty": not bool(value),
        "token_value_printed": False,
    }


def load_token_from_launchctl() -> str:
    try:
        result = subprocess.run(
            ["launchctl", "getenv", "CF_API_TOKEN"],
            text=True,
            capture_output=True,
            timeout=10,
        )
    except Exception:
        return ""
    if result.returncode == 0:
        return result.stdout.strip()
    return ""


def load_token_from_keychain() -> str:
    service_names = [
        "CF_API_TOKEN",
        "CLOUDFLARE_API_TOKEN",
        "cloudflare",
        "cloudflare-api-token",
        "xrmglobalhk-cloudflare-api-token",
        "xrmglobalhk.com-cloudflare-api-token",
    ]
    for service in service_names:
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-s", service, "-w"],
                text=True,
                capture_output=True,
                timeout=10,
            )
        except Exception:
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return ""


def cf_request(method: str, path: str, body: dict | None = None) -> dict:
    data = None
    headers = {
        "Authorization": f"Bearer {token()}",
        "Content-Type": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise CfError(f"Cloudflare API HTTP {exc.code}: {raw[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise CfError(f"Cloudflare API network error: {exc.reason}") from exc

    if not payload.get("success"):
        raise CfError(f"Cloudflare API error: {json.dumps(payload.get('errors'), ensure_ascii=False)}")
    return payload


def get_zone_id() -> str:
    params = urllib.parse.urlencode({"name": ZONE_NAME, "status": "active"})
    payload = cf_request("GET", f"/zones?{params}")
    zones = payload.get("result", [])
    if len(zones) != 1:
        raise CfError(f"Expected exactly one active zone for {ZONE_NAME}, got {len(zones)}.")
    return zones[0]["id"]


def list_all_records(zone_id: str) -> list[dict]:
    records: list[dict] = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"per_page": 100, "page": page})
        payload = cf_request("GET", f"/zones/{zone_id}/dns_records?{params}")
        batch = payload.get("result", [])
        records.extend(batch)
        info = payload.get("result_info", {})
        total_pages = int(info.get("total_pages") or 1)
        if page >= total_pages:
            break
        page += 1
    return records


def is_n8n_record(record: dict) -> bool:
    name = record.get("name", "")
    return name == HOSTNAME or name == RECORD_NAME


def delete_record(zone_id: str, record: dict) -> None:
    cf_request("DELETE", f"/zones/{zone_id}/dns_records/{record['id']}")


def create_good_record(zone_id: str) -> dict:
    payload = {
        "type": "A",
        "name": RECORD_NAME,
        "content": GOOD_IP,
        "ttl": 1,
        "proxied": False,
        "comment": "n8n HTTPS endpoint for xrmglobalhk.com",
    }
    return cf_request("POST", f"/zones/{zone_id}/dns_records", payload)["result"]


def dig(server: str, name: str) -> list[str]:
    cmd = ["dig", f"@{server}", "+short", name, "A"]
    result = subprocess.run(cmd, text=True, capture_output=True, timeout=20)
    if result.returncode != 0:
        raise CfError(f"dig failed for @{server}: {result.stderr.strip()}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def verify_dns() -> dict[str, list[str]]:
    servers = ["mina.ns.cloudflare.com", "nicolas.ns.cloudflare.com", "1.1.1.1", "8.8.8.8"]
    return {server: dig(server, HOSTNAME) for server in servers}


def main() -> int:
    if "--check-config" in sys.argv:
        print(json.dumps(token_state(), indent=2, ensure_ascii=False))
        return 0

    if load_dotenv is None:
        print("Notice: python-dotenv is not installed; using built-in .env fallback parser.")
    print("Step 1/6: Querying Cloudflare zone ID...")
    zone_id = get_zone_id()
    print(f"Zone: {ZONE_NAME}")
    print(f"Zone ID: {zone_id}")

    print("Step 2/6: Listing all DNS records with pagination...")
    records = list_all_records(zone_id)
    n8n_records = [record for record in records if is_n8n_record(record)]
    bad_records = [record for record in n8n_records if record.get("content") == BAD_IP]

    print(f"Total DNS records returned by API: {len(records)}")
    print(f"n8n records returned by API: {len(n8n_records)}")
    for record in n8n_records:
        print(
            "Found n8n record: "
            f"id={record.get('id')} type={record.get('type')} "
            f"name={record.get('name')} content={record.get('content')} "
            f"proxied={record.get('proxied')} ttl={record.get('ttl')}"
        )

    print("Step 3/6: Deleting all API-visible n8n DNS records...")
    for record in n8n_records:
        print(f"Deleting: {record.get('type')} {record.get('name')} {record.get('content')}")
        delete_record(zone_id, record)

    print("Step 4/6: Creating correct DNS-only A record...")
    created = create_good_record(zone_id)
    print(
        "Created: "
        f"id={created.get('id')} type={created.get('type')} "
        f"name={created.get('name')} content={created.get('content')} "
        f"proxied={created.get('proxied')} ttl={created.get('ttl')}"
    )

    print("Step 5/6: Verifying Cloudflare authoritative DNS...")
    deadline = time.time() + 180
    last = {}
    while time.time() < deadline:
        last = verify_dns()
        if all(values == [GOOD_IP] for values in last.values()):
            break
        time.sleep(5)

    print(json.dumps(last, indent=2, ensure_ascii=False))

    print("Step 6/6: Final result...")
    if all(values == [GOOD_IP] for values in last.values()):
        print("SUCCESS: n8n.xrmglobalhk.com resolves to 178.105.167.227 on all required resolvers.")
        return 0

    if not n8n_records and any(BAD_IP in values for values in last.values()):
        print(
            "BLOCKED: Cloudflare API returned no n8n DNS record, but authoritative DNS still returns "
            "172.29.0.127. This indicates a Cloudflare backend shadow/stale/generated record. "
            "Open a Cloudflare Support ticket with the API output and authoritative dig output."
        )
        return 2

    print("FAILED: DNS did not converge to the expected value within 180 seconds.")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Credential checks for the Nightly AI Workflow.

The script reads credentials from environment variables only. Do not commit real
secrets to the repository.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import smtplib
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage


def env(name: str, required: bool = True) -> str:
    value = os.environ.get(name, "").strip()
    if required and not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def request_json(url: str, headers: dict[str, str] | None = None, method: str = "GET") -> dict:
    request = urllib.request.Request(url, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return {"status": response.status, "body": json.loads(body) if body else {}}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def check_google_drive() -> dict:
    token = env("GOOGLE_DRIVE_ACCESS_TOKEN")
    folder_id = env("GOOGLE_DRIVE_WATCH_FOLDER_ID")
    query = urllib.parse.quote(f"'{folder_id}' in parents and trashed=false")
    url = f"https://www.googleapis.com/drive/v3/files?q={query}&pageSize=5&fields=files(id,name,mimeType,modifiedTime)"
    result = request_json(url, headers={"Authorization": f"Bearer {token}"})
    return {"service": "google-drive", "ok": True, "files_seen": len(result["body"].get("files", []))}


def check_github() -> dict:
    token = env("GITHUB_TOKEN")
    owner = env("GITHUB_OWNER")
    repo = env("GITHUB_REPO")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    repo_result = request_json(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    permission = repo_result["body"].get("permissions", {})
    return {
        "service": "github",
        "ok": True,
        "repo": repo_result["body"].get("full_name"),
        "permissions": permission,
        "can_push": bool(permission.get("push")),
    }


def check_cloudflare() -> dict:
    token = env("CLOUDFLARE_API_TOKEN")
    account_id = env("CLOUDFLARE_ACCOUNT_ID")
    project = env("CLOUDFLARE_PAGES_PROJECT")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    verify = request_json("https://api.cloudflare.com/client/v4/user/tokens/verify", headers=headers)
    pages = request_json(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}",
        headers=headers,
    )
    deployment_configs = pages["body"].get("result", {}).get("deployment_configs", {})
    return {
        "service": "cloudflare",
        "ok": bool(verify["body"].get("success") and pages["body"].get("success")),
        "project": pages["body"].get("result", {}).get("name"),
        "production_branch": pages["body"].get("result", {}).get("production_branch"),
        "deployment_configs": deployment_configs,
    }


def check_openai() -> dict:
    token = env("OPENAI_API_KEY")
    result = request_json("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {token}"})
    models = result["body"].get("data", [])
    return {"service": "openai", "ok": True, "models_seen": len(models)}


def check_smtp() -> dict:
    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT"))
    username = env("SMTP_USERNAME")
    password = env("SMTP_PASSWORD")
    sender = env("REVIEW_NOTIFICATION_FROM")
    recipient = env("REVIEW_NOTIFICATION_EMAIL")
    use_ssl = os.environ.get("SMTP_SSL", "false").lower() == "true"

    message = EmailMessage()
    message["Subject"] = "Nightly AI Workflow SMTP Test"
    message["From"] = sender
    message["To"] = recipient
    message.set_content("SMTP credential test succeeded. This is a review notification test.")

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(username, password)
            smtp.send_message(message)

    return {"service": "smtp", "ok": True, "sent_to": recipient}


def check_n8n() -> dict:
    base_url = env("N8N_BASE_URL").rstrip("/")
    api_key = env("N8N_API_KEY")
    headers = {"X-N8N-API-KEY": api_key}
    result = request_json(f"{base_url}/api/v1/workflows", headers=headers)
    workflows = result["body"].get("data", [])
    matching = [wf for wf in workflows if "Nightly" in wf.get("name", "") or "AI Nightly" in wf.get("name", "")]
    return {"service": "n8n", "ok": True, "workflows_seen": len(workflows), "nightly_workflows": matching}


CHECKS = {
    "google-drive": check_google_drive,
    "github": check_github,
    "cloudflare": check_cloudflare,
    "openai": check_openai,
    "smtp": check_smtp,
    "n8n": check_n8n,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Nightly AI Workflow credentials.")
    parser.add_argument("service", choices=sorted(CHECKS.keys()) + ["all"])
    args = parser.parse_args()

    services = sorted(CHECKS.keys()) if args.service == "all" else [args.service]
    results = []
    ok = True
    for service in services:
        try:
            results.append(CHECKS[service]())
        except Exception as exc:
            ok = False
            results.append({"service": service, "ok": False, "error": str(exc)})

    print(json.dumps({"ok": ok, "results": results}, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

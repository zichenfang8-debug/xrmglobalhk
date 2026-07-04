# n8n Local Recovery Report

Date: 2026-07-01

## Scope

Recover the local n8n instance used by the XRM Intelligence Nightly AI Workflow without deleting the existing n8n data folder, workflows, credentials, or SQLite database.

## Protected Data

- n8n user folder: `/Users/zichenfang/Documents/Codex/Clone Repository（克隆仓库）/.n8n-local/.n8n`
- SQLite database: `/Users/zichenfang/Documents/Codex/Clone Repository（克隆仓库）/.n8n-local/.n8n/database.sqlite`
- Backup created before recovery: `/Users/zichenfang/Documents/Codex/Clone Repository（克隆仓库）/.n8n-local/backups/n8n-backup-20260701-restore-point`

No database deletion, workspace reset, workflow deletion, or credential deletion was performed.

## Diagnosis

The original `npx n8n@1.123.62` path was unreliable on this machine because Homebrew Node.js was version 26. Native dependencies failed during install/build when lifecycle scripts used that runtime.

A second issue was caused by the execution sandbox blocking local port binding. Running n8n inside the sandbox produced:

```text
listen EPERM: operation not permitted :::5678
```

This was a sandbox permission problem, not a database corruption problem.

## Fix Applied

- Installed a local n8n runtime under `.n8n-local/runtime` using the Codex bundled Node.js runtime.
- Created `.n8n-local/start-n8n-local.sh` to always start n8n with the compatible Node.js path and the same `N8N_USER_FOLDER`.
- Set `N8N_SECURE_COOKIE=false` for local `http://127.0.0.1:5678` development.
- Added recommended runtime environment variables for SQLite pooling, task runners, environment access behavior, bare Git repository safety, and settings-file permissions.
- Tightened `.n8n-local/.n8n/config` permissions to owner-only read/write.

## Verification Results

- n8n version: `1.123.62`
- Local URL: `http://127.0.0.1:5678`
- HTTP reachability: passed, returned `HTTP/1.1 200 OK`
- Owner login API: passed, returned `HTTP/1.1 200 OK`
- Owner account: `horizonxrm@gmail.com`
- Owner role: `global:owner`
- Workflows found in database: `0`
- Credentials found in database: `0`
- Users found in database: `1`

Because the login API succeeded, no password reset was required.

## Current Operational Note

In this Codex execution environment, detached `nohup` starts were killed when the wrapper command exited. The reliable start method is to run:

```bash
.n8n-local/start-n8n-local.sh
```

from the workspace root, keeping that terminal/session open. A macOS LaunchAgent can be added later if persistent background startup is required.

## Remaining Work

Continue Google Drive credential setup inside n8n:

1. Open `http://127.0.0.1:5678`.
2. Log in as the local Owner account.
3. Create the Google Drive OAuth credential.
4. Complete browser OAuth authorization when prompted.
5. Run the Google Drive read/write verification workflow.

# Nightly AI Workflow Service Setup

This runbook is used service by service. Do not put real secrets in Git.

## Completion Tracker

| Step | Service | Target | Status | Percent |
| --- | --- | --- | --- | --- |
| 1 | Google Drive API | Watched folder readable by n8n | Pending | 0% |
| 2 | GitHub Token | Draft branch and PR creation allowed | Pending | 20% |
| 3 | Cloudflare Pages | Production deploy protected from draft branches | Pending | 40% |
| 4 | OpenAI API | AI analysis endpoint reachable | Pending | 60% |
| 5 | SMTP | Review report email can be sent | Pending | 80% |
| 6 | n8n Credentials | All credentials attached to workflow | Pending | 100% |

## Step 1 - Google Drive API

Goal: n8n can scan a specific Google Drive folder and download supported files.

Manual setup:

1. Open Google Cloud Console.
2. Create or select a project for this automation.
3. Enable Google Drive API.
4. Configure OAuth consent screen.
5. Create OAuth Client ID for n8n.
6. In n8n, create a Google Drive OAuth2 credential.
7. Complete OAuth authorization in n8n.
8. Create a Google Drive folder for nightly intake.
9. Copy the folder ID into `GOOGLE_DRIVE_WATCH_FOLDER_ID`.

Validation:

- In n8n, add or open the Google Drive credential and click reconnect/test.
- Run the workflow manually with one test file in the watched folder.
- Optional script check if you have a temporary OAuth access token:

```bash
GOOGLE_DRIVE_ACCESS_TOKEN=... GOOGLE_DRIVE_WATCH_FOLDER_ID=... \
python3 automation/scripts/check_credentials.py google-drive
```

Completion rule:

- Mark Google Drive complete only when n8n can list the watched folder and download a test file.

## Step 2 - GitHub Token

Goal: n8n can create or update files on a draft branch and open a pull request.

Manual setup:

1. Open GitHub Settings > Developer settings > Fine-grained tokens.
2. Create a fine-grained token for this repository.
3. Grant permissions:
   - Contents: Read and write
   - Pull requests: Read and write
   - Metadata: Read
4. Store the token in n8n GitHub credential.
5. Set `GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_BASE_BRANCH`, and `GITHUB_DRAFT_BRANCH_PREFIX`.

Validation:

```bash
GITHUB_TOKEN=... GITHUB_OWNER=... GITHUB_REPO=... \
python3 automation/scripts/check_credentials.py github
```

Completion rule:

- Mark GitHub complete only when repo metadata is readable and token permissions are sufficient for content writes and PRs.

## Step 3 - Cloudflare Pages

Goal: Cloudflare Pages does not publish draft branches to production.

Manual setup:

1. Open Cloudflare Dashboard > Workers & Pages.
2. Select the Pages project.
3. Confirm production branch is the human-approved branch, usually `main`.
4. Disable automatic production deployment from draft branches.
5. Keep preview deployments allowed if you want PR previews.
6. Create an API token for read verification if desired.
7. Set `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_PAGES_PROJECT`.

Validation:

```bash
CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=... CLOUDFLARE_PAGES_PROJECT=... \
python3 automation/scripts/check_credentials.py cloudflare
```

Completion rule:

- Mark Cloudflare complete only when the Pages project is reachable and production branch is confirmed.

## Step 4 - OpenAI API

Goal: AI classification, extraction, redaction, and drafting endpoint is reachable.

Manual setup:

1. Create or use an OpenAI API key.
2. Store it in n8n OpenAI credential.
3. Set `OPENAI_API_KEY` only in local secret storage or n8n env, not in Git.
4. Confirm model names in `automation/n8n/nightly-ai-workflow.json`.

Validation:

```bash
OPENAI_API_KEY=... python3 automation/scripts/check_credentials.py openai
```

Completion rule:

- Mark OpenAI complete only when a minimal model/API check succeeds.

## Step 5 - SMTP

Goal: n8n can send the daily review report email.

Manual setup:

1. Choose SMTP provider.
2. Create app password or SMTP token.
3. Store SMTP host, port, username, password, and from email in n8n SMTP credential.
4. Set `REVIEW_NOTIFICATION_EMAIL` and `REVIEW_NOTIFICATION_FROM`.

Validation:

```bash
SMTP_HOST=... SMTP_PORT=587 SMTP_USERNAME=... SMTP_PASSWORD=... \
REVIEW_NOTIFICATION_FROM=... REVIEW_NOTIFICATION_EMAIL=... \
python3 automation/scripts/check_credentials.py smtp
```

Completion rule:

- Mark SMTP complete only when a test email can be sent to the review address.

## Step 6 - n8n Credentials

Goal: all credentials are attached to the imported workflow.

Manual setup:

1. Import `automation/n8n/nightly-ai-workflow.json`.
2. Replace all `REPLACE_WITH_N8N_CREDENTIAL_ID` placeholders.
3. Set workflow env vars in n8n.
4. Use manual execution before activating the Cron trigger.

Validation:

```bash
N8N_BASE_URL=... N8N_API_KEY=... \
python3 automation/scripts/check_credentials.py n8n
```

Completion rule:

- Mark n8n complete only when workflow exists, credentials are attached, and manual execution reaches the review report node.

## First Full Test

Use `automation/test-files/nightly-test-source.md` as the test file. Upload it to the Google Drive watched folder, run the n8n workflow manually, and verify:

```text
Google Drive
  -> AI analysis
  -> daily report
  -> website draft
  -> GitHub draft branch
  -> review report email
```

The workflow is not production-ready until every step is checked.

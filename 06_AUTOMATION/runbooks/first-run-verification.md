# First Run Verification

Use this only after every credential is configured.

## Test Input

Upload this file to the Google Drive watched folder:

```text
automation/test-files/nightly-test-source.md
```

## Manual n8n Test

1. Open the imported workflow in n8n.
2. Confirm all credentials are attached.
3. Click Execute Workflow.
4. Confirm the Google Drive node finds the test file.
5. Confirm AI nodes return classification, redaction, and draft data.
6. Confirm GitHub creates a draft branch or PR.
7. Confirm the review email arrives.

## Required Success Chain

```text
Google Drive
  -> AI analysis
  -> generated daily report
  -> generated website draft
  -> GitHub draft branch / PR
  -> review report email
```

## Failure Rules

- If privacy risk is high, stop before GitHub push.
- If AI extraction fails, stop before GitHub push.
- If GitHub push fails, send failure notice.
- If email fails, keep PR open and review n8n execution logs.
- Do not activate the nightly Cron until one manual run succeeds.

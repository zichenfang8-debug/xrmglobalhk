# Production Automation Roadmap

## Objective

Build a production automation platform for XRM Global HK while the public n8n HTTPS endpoint is pending Cloudflare support.

## Priority Order

1. Improve SEO for `xrmglobalhk.com`.
2. Build automatic blog publishing pipeline.
3. Prepare Google Search Console integration.
4. Prepare LinkedIn lead generation workflow.
5. Improve website conversion rate.
6. Build RFQ to AI Review to Supplier Comparison workflow.
7. Design complete n8n workflows locally without requiring HTTPS.

## Operating Mode

Until DNS and HTTPS are fixed, all n8n workflows use one of:

- Manual Trigger
- Cron Trigger
- Local filesystem read/write
- Google Drive polling through existing OAuth credentials

Avoid:

- Public webhook URLs
- Cloudflare DNS edits
- Production deploy triggers
- Auto-publication

## Review Gates

Every workflow must stop before a public action.

Required gates:

- SEO draft review
- Blog content review
- Privacy redaction review
- Supplier shortlist review
- RFQ commercial risk review
- Human approval before publication or outreach

## Standard Output Contract

Every workflow writes a JSON-style result object with:

```json
{
  "generated_by_ai": true,
  "status": "pending-review",
  "workflow_name": "",
  "run_date": "",
  "source": "",
  "outputs": [],
  "privacy_flags": [],
  "review_checklist": []
}
```

## Non-Goals

- Do not fix Cloudflare DNS until Cloudflare replies.
- Do not configure public n8n HTTPS.
- Do not publish website content automatically.
- Do not send LinkedIn messages automatically.
- Do not commit or expose secrets.

## Next Milestones

1. Import local n8n workflow JSON files.
2. Run each with Manual Trigger and sample input.
3. Confirm all outputs are draft-only.
4. Replace sample data with Google Drive or Google Sheets sources.
5. Add production credentials only after manual review.

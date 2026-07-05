# XRM Production Automation Platform

This folder contains reusable automation infrastructure for XRM Global HK.

Current priority: build production-ready workflows locally without requiring public HTTPS. All workflows are draft-first and review-gated.

## Safety Rules

- Do not publish automatically.
- Do not modify production DNS.
- Do not read or edit `.env` from workflow design files.
- Do not commit secrets.
- Do not overwrite existing website pages.
- Do not delete pages or images.
- All AI-generated public content must go to a draft or pending-review path first.
- Every workflow must produce a review checklist before any human-approved publication step.

## Local Workflow Strategy

Use local n8n manual triggers while `n8n.xrmglobalhk.com` DNS is pending Cloudflare support.

Draft output paths:

```text
content/drafts/
content/pending-review/
03_CONTENT/_drafts/
automation/reports/
```

Approved archive paths:

```text
03_CONTENT/seo-articles/
03_CONTENT/social-posts/
03_CONTENT/website-copy/
```

## Workflow Files

```text
automation/n8n/seo-blog-pipeline-local.json
automation/n8n/google-search-console-prep-local.json
automation/n8n/linkedin-lead-generation-local.json
automation/n8n/rfq-ai-review-supplier-comparison-local.json
```

## Runbooks

```text
automation/runbooks/production-automation-roadmap.md
automation/runbooks/seo-optimization-plan.md
automation/runbooks/blog-publishing-pipeline.md
automation/runbooks/google-search-console-integration.md
automation/runbooks/linkedin-lead-generation-workflow.md
automation/runbooks/conversion-rate-optimization.md
automation/runbooks/rfq-ai-supplier-comparison-workflow.md
```

## Prompt Files

```text
automation/prompts/seo-audit.prompt.md
automation/prompts/blog-article-generator.prompt.md
automation/prompts/google-search-console-insight.prompt.md
automation/prompts/linkedin-lead-qualifier.prompt.md
automation/prompts/conversion-copy-review.prompt.md
automation/prompts/rfq-ai-review.prompt.md
automation/prompts/supplier-comparison.prompt.md
```

## Local Helper Scripts

```text
automation/scripts/seo_metadata_validator.py
automation/scripts/generate_blog_review_checklist.py
```

The helper scripts are intentionally local-only. They do not publish, push, deploy, or call external APIs.

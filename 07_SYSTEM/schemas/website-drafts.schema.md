# Website Drafts Schema

Compatible with Google Sheets, Notion, and CSV.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| draft_id | text | yes | Stable ID, for example `WEB-DRAFT-YYYYMMDD-001`. |
| generated_by_ai | boolean | yes | Always `true` for automation drafts. |
| status | select | yes | `pending-review`, `approved`, `rejected`, `published`. |
| source_file_ids | text | no | Source Google Drive file IDs. |
| content_type | select | yes | `article`, `case_draft`, `service_page`, `supplier_profile`, `social_post`, `other`. |
| title | text | yes | Draft title. |
| recommended_path | text | yes | Draft path under `content/pending-review/` or `content/drafts/`. |
| target_public_path | text | no | Future public path after approval. |
| business_area | text | no | China supply chain, hotel procurement, AI infrastructure, etc. |
| language | select | no | `en`, `zh`, `bilingual`. |
| summary | text | no | Short summary. |
| seo_keywords | text | no | Comma-separated keywords. |
| privacy_flags | text | yes | Sensitive items detected. |
| human_required_changes | text | no | Edits required before approval. |
| approved_by | text | no | Human approver. |
| approved_at | date | no | Approval date. |
| published_commit | text | no | Commit hash after publication. |
| last_updated | date | yes | Last update date. |

# Daily Actions Schema

Compatible with Google Sheets, Notion, and CSV.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| action_id | text | yes | Stable ID, for example `ACT-YYYYMMDD-001`. |
| generated_by_ai | boolean | yes | Always `true` for automation drafts. |
| status | select | yes | `pending-review`, `approved`, `done`, `deferred`, `rejected`. |
| source_file_ids | text | no | Source Google Drive file IDs. |
| priority | select | yes | `urgent`, `high`, `medium`, `low`. |
| action_type | select | yes | `supplier-follow-up`, `quote-check`, `hotel-procurement`, `website-review`, `social-review`, `data-cleanup`, `research`, `other`. |
| owner | text | no | Person responsible. |
| due_date | date | no | Target date. |
| task | text | yes | Action item. |
| context | text | no | Why this action matters. |
| expected_output | text | no | Deliverable or decision needed. |
| related_supplier_id | text | no | Supplier reference. |
| related_project_id | text | no | Project reference. |
| privacy_flags | text | yes | Sensitive items detected. |
| reviewed_by | text | no | Human reviewer. |
| reviewed_at | date | no | Review date. |
| last_updated | date | yes | Last update date. |

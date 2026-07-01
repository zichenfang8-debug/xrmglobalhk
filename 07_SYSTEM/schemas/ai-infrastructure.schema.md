# AI Infrastructure Schema

Compatible with Google Sheets, Notion, and CSV.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| record_id | text | yes | Stable ID, for example `AI-INFRA-YYYYMMDD-001`. |
| generated_by_ai | boolean | yes | Always `true` for automation drafts. |
| status | select | yes | `pending-review`, `approved`, `rejected`, `needs-research`. |
| source_file_ids | text | no | Source Google Drive file IDs. |
| category | select | yes | `data_center`, `server`, `gpu`, `cooling`, `power`, `cabling`, `rack`, `network`, `construction`, `other`. |
| item_or_topic | text | yes | Item, component, or topic. |
| supplier_candidate | text | no | Supplier or manufacturer candidate. |
| specification | text | no | Technical specification. |
| capacity_or_rating | text | no | Power, cooling, throughput, rack units, etc. |
| compliance_or_standard | text | no | Standard, certification, or regulation. |
| country_region | text | no | Region relevance. |
| thailand_sea_relevance | text | no | Thailand / Southeast Asia relevance. |
| supply_chain_notes | text | no | Availability, lead time, risk, substitution. |
| price_signal | text | no | Public-safe price signal. |
| risk_level | select | no | `low`, `medium`, `high`, `unknown`. |
| evidence | text | no | Source evidence summary. |
| privacy_flags | text | yes | Sensitive items detected. |
| next_actions | text | no | Follow-up tasks. |
| reviewed_by | text | no | Human reviewer. |
| reviewed_at | date | no | Review date. |
| last_updated | date | yes | Last update date. |

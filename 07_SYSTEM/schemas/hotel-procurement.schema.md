# Hotel Procurement Schema

Compatible with Google Sheets, Notion, and CSV.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| item_id | text | yes | Stable item ID, for example `HOTEL-YYYYMMDD-001`. |
| generated_by_ai | boolean | yes | Always `true` for automation drafts. |
| status | select | yes | `pending-review`, `approved`, `rejected`, `needs-quote`, `ordered`. |
| source_file_ids | text | no | Source Google Drive file IDs. |
| project_placeholder | text | yes | Public-safe project placeholder. |
| real_project_name_internal | text | no | Internal-only review field. Never export externally. |
| area_or_room_type | text | no | Lobby, guestroom, BOH, restaurant, etc. |
| classification | select | yes | `FF&E`, `OS&E`, `construction_related`, `unknown`. |
| item_name | text | yes | Product or procurement item. |
| specification | text | no | Technical or design specification. |
| material | text | no | Material or finish. |
| dimensions | text | no | Dimensions. |
| quantity | number | no | Quantity. |
| unit | text | no | Unit of measure. |
| target_price | number | no | Target price. |
| quoted_price | number | no | Quoted price. |
| currency | text | no | Currency code. |
| supplier_candidate | text | no | Candidate supplier display name. |
| lead_time | text | no | Lead time. |
| quality_requirement | text | no | Inspection or performance requirement. |
| logistics_packaging_notes | text | no | Shipping, packaging, or installation notes. |
| privacy_flags | text | yes | Sensitive items detected. |
| open_questions | text | no | Questions for reviewer or supplier. |
| reviewed_by | text | no | Human reviewer. |
| reviewed_at | date | no | Review date. |
| last_updated | date | yes | Last update date. |

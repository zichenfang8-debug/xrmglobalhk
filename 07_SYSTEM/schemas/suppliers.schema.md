# Suppliers Schema

Compatible with Google Sheets, Notion, and CSV.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| supplier_id | text | yes | Stable internal ID, for example `SUP-YYYYMMDD-001`. |
| generated_by_ai | boolean | yes | Always `true` for automation drafts. |
| status | select | yes | `pending-review`, `approved`, `rejected`, `needs-follow-up`. |
| source_file_ids | text | no | Comma-separated Google Drive file IDs. |
| supplier_name_internal | text | no | Internal name for review only. |
| supplier_name_public | text | yes | Public-safe or anonymized supplier display name. |
| country_region | text | no | Country or region. |
| city_province | text | no | City or province. |
| business_type | select | no | `factory`, `trading-company`, `agent`, `unknown`. |
| product_categories | text | no | Comma-separated categories. |
| hotel_ff_e_relevance | text | no | FF&E relevance notes. |
| hotel_os_e_relevance | text | no | OS&E relevance notes. |
| ai_infrastructure_relevance | text | no | AI/data center relevance notes. |
| certifications | text | no | Certifications or standards. |
| moq | text | no | Minimum order quantity. |
| lead_time | text | no | Production or delivery lead time. |
| price_level | select | no | `low`, `mid`, `high`, `unknown`. |
| currency | text | no | Currency code. |
| incoterms | text | no | EXW, FOB, CIF, DDP, etc. |
| export_experience | text | no | Export market notes. |
| quality_notes | text | no | QC risks or strengths. |
| privacy_flags | text | yes | Any detected sensitive items. |
| missing_fields | text | no | Fields needing manual follow-up. |
| next_actions | text | no | Suggested next steps. |
| reviewed_by | text | no | Human reviewer. |
| reviewed_at | date | no | Review date. |
| last_updated | date | yes | Last update date. |

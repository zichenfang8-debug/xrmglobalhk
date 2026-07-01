# Schema: 全球酒店项目数据库

**版本**: v1.0
**创建**: 2026-07-01
**对应目录**: `01_DATABASES/hotel-projects/`

---

## 字段定义

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `project_id` | string | ✅ | 唯一ID，格式 `HTL-YYYYMM-001` |
| `project_alias` | string | ✅ | 代称（不含客户真实名），如 `Bangkok 5-Star Resort 2026` |
| `hotel_brand_group` | string | ❌ | 酒店集团，如 `Marriott` / `Hilton` / `Independent` |
| `star_rating` | integer | ✅ | 1-5 |
| `hotel_type` | enum | ✅ | `resort` / `city-hotel` / `boutique` / `serviced-apartment` / `mixed-use` |
| `country` | string | ✅ | ISO 3166-1 alpha-2，如 `TH` |
| `city` | string | ✅ | 城市名 |
| `region` | enum | ✅ | `SEA` / `Middle East` / `China` / `Other` |
| `project_type` | enum | ✅ | `new-build` / `renovation` / `expansion` / `refurbishment` |
| `scope` | array[enum] | ✅ | `["FFE", "OSE"]` 或其中之一 |
| `room_count` | integer | ❌ | 客房数量 |
| `budget_range_usd` | string | ❌ | 如 `"500K-1M"` / `"1M-5M"` / `">5M"` |
| `procurement_stage` | enum | ✅ | `lead` / `rfq-sent` / `quoted` / `negotiation` / `awarded` / `in-production` / `delivered` / `completed` |
| `target_delivery` | string | ❌ | 格式 `YYYY-MM` |
| `epc_contractor` | string | ❌ | EPC 总包商（可用代称） |
| `me_contractor` | string | ❌ | M&E 分包商（可用代称） |
| `id_firm` | string | ❌ | 室内设计公司 |
| `xrm_role` | enum | ❌ | `prime-supplier` / `sub-supplier` / `sourcing-only` |
| `categories_supplied` | array[string] | ❌ | 如 `["mattress", "furniture", "lighting"]` |
| `notes` | string | ❌ | 自由文本备注（不含客户姓名和保密信息） |
| `source` | string | ✅ | 信息来源 |
| `created_at` | string | ✅ | 格式 `YYYY-MM-DD` |
| `updated_at` | string | ✅ | 格式 `YYYY-MM-DD` |

---

## 示例 JSON

```json
{
  "project_id": "HTL-202607-001",
  "project_alias": "Phuket Luxury Resort Renovation 2026",
  "hotel_brand_group": "Independent",
  "star_rating": 5,
  "hotel_type": "resort",
  "country": "TH",
  "city": "Phuket",
  "region": "SEA",
  "project_type": "renovation",
  "scope": ["FFE", "OSE"],
  "room_count": 120,
  "budget_range_usd": "1M-5M",
  "procurement_stage": "quoted",
  "target_delivery": "2026-12",
  "epc_contractor": "Thai Contractor A",
  "me_contractor": "",
  "id_firm": "Bangkok Design Studio B",
  "xrm_role": "prime-supplier",
  "categories_supplied": ["bedroom furniture", "bathroom accessories", "soft furnishings"],
  "notes": "",
  "source": "referral",
  "created_at": "2026-07-01",
  "updated_at": "2026-07-01"
}
```

---

## 变更历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-07-01 | 初始创建 |

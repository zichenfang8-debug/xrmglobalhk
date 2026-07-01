# Schema: EPC / M&E / 建筑设计公司数据库

**版本**: v1.0
**创建**: 2026-07-01
**对应目录**: `01_DATABASES/epc-me-firms/`

---

## 字段定义

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `firm_id` | string | ✅ | 唯一ID，格式 `EPC-YYYYMM-001` |
| `company_name` | string | ✅ | 公司正式名称 |
| `firm_type` | enum | ✅ | `EPC` / `ME` / `ID` / `Architect` / `PMC` |
| `country` | string | ✅ | 注册国家（ISO 3166-1 alpha-2，如 `TH`） |
| `city` | string | ✅ | 主要运营城市 |
| `region` | enum | ✅ | `SEA` / `Middle East` / `China` / `Global` |
| `specialization` | array[string] | ✅ | 专业领域，如 `["hotel", "data center", "commercial"]` |
| `employee_count` | enum | ❌ | `<50` / `50-200` / `200-1000` / `>1000` |
| `annual_revenue_usd` | string | ❌ | 如 `"50M-100M"`，不填精确数字 |
| `notable_projects` | array[object] | ❌ | 已完成代表项目（见子字段） |
| `notable_projects[].project_name` | string | — | 项目名称（可使用代称） |
| `notable_projects[].location` | string | — | 项目地点 |
| `notable_projects[].year` | integer | — | 竣工年份 |
| `key_contact_name` | string | ❌ | 关键联系人姓名 |
| `key_contact_title` | string | ❌ | 职位 |
| `contact_email` | string | ❌ | 联系邮箱 |
| `website` | string | ❌ | 公司官网 URL |
| `linkedin` | string | ❌ | LinkedIn 公司页面 |
| `relationship_status` | enum | ✅ | `prospect` / `contacted` / `meeting-held` / `partner` / `inactive` |
| `first_contact_date` | string | ❌ | 格式 `YYYY-MM-DD` |
| `last_interaction_date` | string | ❌ | 格式 `YYYY-MM-DD` |
| `procurement_influence` | enum | ❌ | `specifier` / `decision-maker` / `influencer` / `unknown` |
| `notes` | string | ❌ | 自由文本备注 |
| `source` | string | ✅ | 信息来源，如 `linkedin`/`exhibition`/`referral`/`manual` |
| `created_at` | string | ✅ | 格式 `YYYY-MM-DD` |
| `updated_at` | string | ✅ | 格式 `YYYY-MM-DD` |

---

## 示例 JSON

```json
{
  "firm_id": "EPC-202607-001",
  "company_name": "Example Construction Co. Ltd.",
  "firm_type": "EPC",
  "country": "TH",
  "city": "Bangkok",
  "region": "SEA",
  "specialization": ["hotel", "resort", "commercial"],
  "employee_count": "200-1000",
  "notable_projects": [
    {
      "project_name": "5-Star Resort Phuket",
      "location": "Phuket, Thailand",
      "year": 2024
    }
  ],
  "key_contact_name": "",
  "contact_email": "",
  "website": "",
  "relationship_status": "prospect",
  "procurement_influence": "specifier",
  "notes": "",
  "source": "exhibition",
  "created_at": "2026-07-01",
  "updated_at": "2026-07-01"
}
```

---

## 变更历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-07-01 | 初始创建 |

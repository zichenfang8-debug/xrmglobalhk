# 01_DATABASES/suppliers — 全球供应商数据库

## 用途
记录 XRM 合作过或评估过的全球供应商信息。
涵盖中国制造商、泰国本地供应商、东南亚和中东地区分销商。

## 品类范围
- 酒店 FF&E（家具、固定装置、设备）
- 酒店 OS&E（运营用品）
- AI 基础设施 / 数据中心设备
- 电气设备 / 工业产品
- 建筑材料

## 文件命名
```
YYYY-MM-DD-[来源]-[品类]-[地区].json
例：2026-07-01-alibaba-fffe-china.json
例：2026-07-15-manual-datacenter-thailand.json
```

## JSON 字段（遵循 07_SYSTEM/schemas/suppliers.schema.md）
```json
{
  "supplier_id": "SUP-YYYYMM-001",
  "name": "",
  "country": "",
  "city": "",
  "product_categories": [],
  "certifications": [],
  "contact_email": "",
  "website": "",
  "price_tier": "low|mid|high",
  "lead_time_days": 0,
  "moq": "",
  "notes": "",
  "source": "manual|alibaba|referral|exhibition",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD",
  "status": "active|inactive|blacklisted"
}
```

## AI 更新规则
- 新供应商：新建 JSON 文件或追加到当日文件
- 更新供应商：修改对应条目，更新 `updated_at`
- 月度快照：每月1日生成 `YYYY-MM-suppliers-snapshot.json`

# 01_DATABASES/hotel-projects — 全球酒店项目数据库

## 用途
追踪全球酒店 FF&E / OS&E 采购项目信息，包括已完成、进行中、潜在项目。
用于市场分析、客户开发、历史报价参考。

## 地区覆盖
- 泰国（重点）
- 东南亚（越南、柬埔寨、印尼、马来西亚）
- 中东（沙特、UAE、卡塔尔）
- 其他

## 文件命名
```
YYYY-MM-DD-[地区]-[项目类型].json
例：2026-07-01-thailand-resort-pipeline.json
例：2026-Q3-middle-east-hotel-projects.json
```

## JSON 字段（遵循 07_SYSTEM/schemas/hotel-procurement.schema.md）
```json
{
  "project_id": "HTL-YYYYMM-001",
  "project_name": "[隐去真实客户名]",
  "hotel_brand": "",
  "star_rating": 0,
  "country": "",
  "city": "",
  "project_type": "new-build|renovation|expansion",
  "scope": ["FFE", "OSE"],
  "room_count": 0,
  "budget_range_usd": "",
  "procurement_stage": "lead|rfq|quoted|awarded|completed",
  "target_delivery": "YYYY-MM",
  "epc_contractor": "",
  "me_contractor": "",
  "notes": "",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## 保密规定
- **不记录客户公司名称**，以 `[Hotel Brand] [City] Project` 形式代替
- **不记录合同金额**，只记录预算范围区间

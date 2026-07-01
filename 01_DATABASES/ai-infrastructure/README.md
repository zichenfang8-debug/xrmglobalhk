# 01_DATABASES/ai-infrastructure — AI 基础设施数据库

## 用途
追踪全球 AI 基础设施、数据中心、算力相关产品与供应商。
支持 XRM 在 AI 硬件采购、数据中心建设方面的业务拓展。

## 品类范围
- GPU 服务器 / AI 计算节点
- 数据中心机柜、PDU、UPS
- 液冷 / 风冷散热系统
- 高压直流（HVDC）供电系统
- 光模块 / 交换机 / 网络设备
- 储能系统（BESS）

## 文件命名
```
YYYY-MM-DD-[品类]-[来源].json
例：2026-07-01-gpu-servers-china-suppliers.json
例：2026-07-01-datacenter-cooling-market-report.md
```

## JSON 字段（遵循 07_SYSTEM/schemas/ai-infrastructure.schema.md）
```json
{
  "record_id": "AI-YYYYMM-001",
  "product_type": "",
  "product_name": "",
  "supplier": "",
  "country_of_origin": "",
  "key_specs": {},
  "certifications": [],
  "price_range_usd": "",
  "lead_time_weeks": 0,
  "target_market": ["Thailand", "Middle East", "SEA"],
  "notes": "",
  "source": "",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## AI 更新规则
- 每次研究新产品或供应商，追加到当月 JSON 文件
- 市场报告存为 `.md` 文件，同步到 `04_INTELLIGENCE/market-reports/`

# 01_DATABASES/epc-me-firms — EPC / M&E / 建筑设计公司数据库

## 用途
收录全球（重点东南亚、中东）EPC 总包商、M&E 机电分包商、建筑设计公司信息。
这类公司是 XRM 的重要间接客户——他们指定采购、XRM 供货。

## 公司类型
| 类型 | 说明 |
|------|------|
| EPC | Engineering, Procurement & Construction 总包商 |
| M&E | Mechanical & Electrical 机电分包商 |
| ID Firm | Interior Design 室内设计公司 |
| Architect | 建筑设计事务所 |
| PMC | Project Management Consultant |

## 文件命名
```
YYYY-MM-DD-[地区]-[公司类型]-firms.json
例：2026-07-01-thailand-epc-firms.json
例：2026-07-01-middle-east-me-contractors.json
```

## JSON 字段
```json
{
  "firm_id": "EPC-YYYYMM-001",
  "company_name": "",
  "firm_type": "EPC|ME|ID|Architect|PMC",
  "country": "",
  "city": "",
  "specialization": [],
  "notable_projects": [],
  "key_contact": "",
  "contact_email": "",
  "website": "",
  "relationship_status": "prospect|contacted|partner",
  "notes": "",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## AI 更新规则
- 每次接触新 EPC/M&E 公司，创建或追加记录
- 每季度更新 `relationship_status`
- 已完成合作的项目记录同步到 `01_DATABASES/hotel-projects/`

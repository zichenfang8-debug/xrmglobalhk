# 02_PROCUREMENT — 采购工作区

## 用途
XRM 采购业务的操作中心：知识库、模板库、进行中项目。

## 子目录

| 目录 | 用途 |
|------|------|
| `knowledge-base/` | 采购知识库：品类知识、行业标准、操作规程 |
| `rfq-templates/` | RFQ 询价模板库（按品类分类） |
| `quotation-templates/` | 报价模板库（PI / CI / Offer Sheet） |
| `active-projects/` | 进行中的采购项目文件 |

## 工作流
```
客户需求 → active-projects/ 新建项目文件
         → rfq-templates/ 选择对应模板
         → 发出 RFQ
         → 收到报价 → 整理进 active-projects/
         → 最终 PI/CI 归档到 05_DOCUMENTS/
```

## AI 更新规则
- 每完成一个项目，在 `knowledge-base/` 沉淀一条品类经验
- 每次使用模板后如有改进，更新对应模板文件版本号
- `active-projects/` 项目完成后，移动摘要到 `01_DATABASES/hotel-projects/`

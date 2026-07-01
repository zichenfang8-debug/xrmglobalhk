# 07_SYSTEM — 系统配置与索引

## 用途
XRM Intelligence 系统的元数据层：Schema 定义、系统索引、全局配置。
这是系统的"说明书"——所有 AI 和人工操作都应先查阅此处的规则。

## 子目录

| 目录 | 用途 |
|------|------|
| `schemas/` | 所有数据库的 JSON/Markdown Schema 定义 |
| `index/` | 系统主索引、变更日志、目录地图 |
| `config/` | 全局配置（AI 参数、命名规则、版本标准） |

## 核心文件

| 文件 | 用途 |
|------|------|
| `index/MASTER_INDEX.md` | 系统总览和目录导航（入口文件） |
| `schemas/suppliers.schema.md` | 供应商数据库字段定义 |
| `schemas/hotel-procurement.schema.md` | 酒店采购数据库字段定义 |
| `schemas/ai-infrastructure.schema.md` | AI基础设施数据库字段定义 |
| `schemas/epc-me-firms.schema.md` | EPC/M&E公司数据库字段定义 |

## AI 更新规则
- 新增数据库或字段：先更新 Schema，再写入数据
- 目录结构调整：先更新 MASTER_INDEX.md，再执行操作
- 所有 Schema 变更须包含版本号和变更日期

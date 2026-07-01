# 05_DOCUMENTS — 商业文件归档

## 用途
存储 XRM 已实际使用的正式商业文件（非模板）。
模板文件存放在 `02_PROCUREMENT/rfq-templates/` 和 `02_PROCUREMENT/quotation-templates/`。

## 子目录

| 目录 | 文件类型 | 说明 |
|------|----------|------|
| `CI/` | Commercial Invoice | 已签发的商业发票 |
| `PI/` | Proforma Invoice | 已签发的形式发票 |
| `RFQ/` | Request for Quotation | 已发出的询价单 |

## 文件命名
```
[类型]-[项目代码]-[日期]-[版本].[docx/xlsx/pdf]
例：PI-PRJ2026001-2026-07-01-v1.docx
例：CI-PRJ2026001-2026-07-15-v1.pdf
例：RFQ-PRJ2026001-2026-07-01.docx
```

## 保密规定
- 存档前**必须移除**客户名称、联系方式
- 以项目代码（PRJ-YYYY-XXX）替代客户标识
- 不存储含有公司印章的扫描件

## AI 更新规则
- 文件由人工生成并审核后存入此目录
- AI 不自动写入此目录
- 每季度：检查旧文件，确认归档完整性

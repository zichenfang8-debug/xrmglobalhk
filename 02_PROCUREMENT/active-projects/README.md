# 02_PROCUREMENT/active-projects — 进行中的采购项目

## 用途
存储每个正在执行的采购项目的工作文件：询价记录、报价对比、跟进日志。
项目完成后，摘要数据迁移到 `01_DATABASES/hotel-projects/`。

## 文件命名
```
[项目代码]-[日期]-[文件类型].json|md
例：PRJ-2026-001-2026-07-01-rfq-log.md
例：PRJ-2026-001-2026-07-15-quote-comparison.xlsx
```

## 项目代码规则
```
PRJ-[年份]-[序号]
例：PRJ-2026-001（2026年第1个项目）
```

## 项目文件夹结构（每个项目一个子文件夹）
```
PRJ-2026-001/
├── project-brief.md       ← 项目概述（品类、数量、交期、预算范围）
├── rfq-sent/              ← 已发出的询价单
├── quotes-received/       ← 收到的供应商报价
├── quote-comparison.xlsx  ← 报价对比表
└── correspondence/        ← 往来邮件摘要（隐去客户信息）
```

## AI 更新规则
- 每次与供应商互动，更新对应项目的 correspondence/ 或 rfq-log
- 项目完成时：提取关键数据 → 写入 `01_DATABASES/hotel-projects/` → 本目录归档
- 归档方式：重命名为 `PRJ-2026-001-COMPLETED/`，不删除

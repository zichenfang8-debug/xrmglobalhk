# 04_INTELLIGENCE — XRM 商业情报中心

## 用途
XRM 的市场研究、竞争情报、行业趋势追踪中心。
所有研究报告用**中文**撰写，供内部决策使用。

## 子目录

| 目录 | 用途 |
|------|------|
| `market-reports/` | 市场研究报告（品类、地区、行业） |
| `competitor-analysis/` | 竞争对手分析 |
| `industry-trends/` | 行业趋势追踪（AI、酒店、数据中心） |
| `nightly-reports/` | 自动化每日/每周情报报告 |

## 报告命名
```
YYYY-MM-DD-[主题]-[类型].md
例：2026-07-01-thailand-hotel-market-Q2-report.md
例：2026-07-15-ai-datacenter-china-suppliers-analysis.md
```

## 报告模板结构
```markdown
# [报告标题]
**日期**: YYYY-MM-DD
**来源**: [数据来源]
**摘要**: [3句话核心结论]

## 市场概况
## 关键发现
## 供应商/竞争对手动态
## XRM 的机会与风险
## 建议行动
```

## AI 自动更新规则
- `nightly-reports/`：由 n8n 自动化工作流每日生成，命名 `YYYY-MM-DD-ai-nightly-report.md`
- 其他报告：手动触发或基于特定事件生成
- 所有报告**只追加，不覆盖**
- 关键数据点同步更新到 `01_DATABASES/` 对应数据库

# XRM Intelligence — Master Index

**系统版本**: v1.0
**建立日期**: 2026-07-01
**维护规则**: 每次目录结构变更时，AI 必须同步更新此文件

---

## 系统定位

XRM Intelligence 是 XRM GLOBAL TRADE LIMITED 的全球采购商业操作系统（Business Operating System）。
覆盖：全球供应商数据库、酒店采购、AI基础设施、内容营销、商业情报。

---

## 目录地图

```
XRM-Intelligence/
├── 01_DATABASES/          ← 全球数据库中心（最核心资产）
│   ├── suppliers/         ← 全球供应商库
│   ├── hotel-projects/    ← 酒店项目库
│   ├── ai-infrastructure/ ← AI基础设施库
│   └── epc-me-firms/      ← EPC/M&E/设计公司库
│
├── 02_PROCUREMENT/        ← 采购工作区
│   ├── knowledge-base/    ← 采购知识库
│   ├── rfq-templates/     ← RFQ模板库
│   ├── quotation-templates/ ← 报价模板库
│   └── active-projects/   ← 进行中项目
│
├── 03_CONTENT/            ← 内容生产线
│   ├── seo-articles/      ← 已发布SEO文章
│   ├── website-copy/      ← 网站文案
│   ├── social-posts/      ← 社媒内容
│   └── _drafts/           ← 草稿区
│
├── 04_INTELLIGENCE/       ← 商业情报中心
│   ├── market-reports/    ← 市场报告
│   ├── competitor-analysis/ ← 竞争对手分析
│   ├── industry-trends/   ← 行业趋势
│   └── nightly-reports/   ← 自动化情报报告
│
├── 05_DOCUMENTS/          ← 商业文件归档
│   ├── CI/                ← 商业发票
│   ├── PI/                ← 形式发票
│   └── RFQ/               ← 询价单
│
├── 06_AUTOMATION/         ← 自动化引擎
│   ├── prompts/           ← AI提示词
│   ├── scripts/           ← Python脚本
│   ├── n8n/               ← n8n工作流
│   ├── runbooks/          ← 操作手册
│   ├── setup/             ← 服务配置
│   └── test-files/        ← 测试样本
│
└── 07_SYSTEM/             ← 系统配置
    ├── schemas/           ← 数据Schema定义
    ├── index/             ← 系统索引（本目录）
    └── config/            ← 全局配置
```

---

## Schema 索引

| Schema 文件 | 对应数据库 | 版本 |
|-------------|-----------|------|
| `suppliers.schema.md` | `01_DATABASES/suppliers/` | 见文件 |
| `hotel-procurement.schema.md` | `01_DATABASES/hotel-projects/` | 见文件 |
| `hotel-projects.schema.md` | `01_DATABASES/hotel-projects/` | v1.0 |
| `ai-infrastructure.schema.md` | `01_DATABASES/ai-infrastructure/` | 见文件 |
| `epc-me-firms.schema.md` | `01_DATABASES/epc-me-firms/` | v1.0 |
| `content.schema.md` | `03_CONTENT/` | v1.0 |
| `daily-actions.schema.md` | `06_AUTOMATION/` | 见文件 |
| `website-drafts.schema.md` | `03_CONTENT/_drafts/` | 见文件 |

---

## 模板索引

| 模板类型 | 目录 | 当前数量 |
|----------|------|----------|
| RFQ 询价模板 | `02_PROCUREMENT/rfq-templates/` | 待建立 |
| PI/报价模板 | `02_PROCUREMENT/quotation-templates/` | 待建立 |
| AI 提示词 | `06_AUTOMATION/prompts/` | 7个 |

---

## 数据库状态

| 数据库 | 目录 | 记录数 | 最后更新 |
|--------|------|--------|----------|
| 供应商数据库 | `01_DATABASES/suppliers/` | — | 2026-07-01 |
| 酒店项目数据库 | `01_DATABASES/hotel-projects/` | — | — |
| AI基础设施数据库 | `01_DATABASES/ai-infrastructure/` | — | — |
| EPC/M&E公司数据库 | `01_DATABASES/epc-me-firms/` | — | — |

---

## AI 操作协议

### 写入规则
1. **只追加，不覆盖** — 已有数据文件只能追加新条目或更新字段
2. **先查 Schema** — 写入任何数据库前，先读取 `07_SYSTEM/schemas/` 对应 Schema
3. **先查 Index** — 执行目录操作前，先读取本文件
4. **更新时间戳** — 每次更新数据，必须更新 `updated_at` 字段
5. **不保存保密信息** — 客户名称、合同金额、联系方式不写入数据库

### 每日自动化检查清单
- [ ] `04_INTELLIGENCE/nightly-reports/` 有当日报告
- [ ] `01_DATABASES/` 有新数据条目或更新
- [ ] `03_CONTENT/_drafts/` 有新草稿（如有内容任务）
- [ ] 本 Index 文件已同步最新状态

### 命名约定
```
数据文件:   YYYY-MM-DD-[来源/主题]-[类型].json
报告文件:   YYYY-MM-DD-[主题]-report.md
模板文件:   [类型]-TEMPLATE-[品类]-v[N].[ext]
项目文件:   PRJ-YYYY-NNN-[描述].[ext]
```

---

## 变更日志

| 日期 | 版本 | 变更说明 | 操作者 |
|------|------|----------|--------|
| 2026-07-01 | v1.0 | 初始建立 XRM Intelligence 系统目录结构 | Claude AI |

---

*此文件由 AI 维护。每次系统结构变更后自动更新。*

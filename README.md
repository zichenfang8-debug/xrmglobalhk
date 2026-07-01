# XRM GLOBAL TRADE LIMITED

## Company Introduction

XRM GLOBAL TRADE LIMITED is building a structured digital workspace for international trade, cross-border procurement, hotel supply chain management, business documentation, and AI-assisted operations.

This repository is the official long-term workspace for the company's website foundation, procurement knowledge base, automation scripts, operating documents, and reusable AI prompts.

## Business Scope

XRM GLOBAL TRADE LIMITED focuses on connecting international buyers with reliable China-based sourcing, procurement, documentation, and trade execution support.

Key areas include:

- China Supply Chain
- Hotel FF&E
- Hotel OS&E
- Cross-border Procurement
- International Trade
- Supplier and product research
- Business document preparation
- AI-supported workflow automation

## China Supply Chain

The repository will organize knowledge, supplier records, product categories, templates, and operating procedures related to China supply chain sourcing and coordination.

## Hotel FF&E

Hotel FF&E procurement materials will be organized under the procurement knowledge base, including product categories, supplier references, specifications, quotation workflows, and project documentation.

## Hotel OS&E

Hotel OS&E resources will support repeatable procurement workflows for hotel operating supplies and equipment, including supplier comparison, product lists, and request-for-quotation materials.

## Cross-border Procurement

This workspace will support cross-border procurement processes such as supplier sourcing, quotation management, invoice documentation, purchase coordination, logistics references, and quality-control records.

## International Trade

International trade documentation, commercial templates, procurement records, and operational knowledge will be maintained here for long-term company use.

## Repository Structure

```text
website/
  pages/
  assets/
    images/
    css/
    js/

blog/

docs/
  PI/
  CI/
  RFQ/
  Templates/

procurement/
  Hotel/
  Suppliers/
  Products/

knowledge-base/

automation/
  scripts/

prompts/
  Claude/
  Codex/
```

## Future Roadmap

Planned development areas include:

- Website content and Cloudflare Pages deployment
- Blog and company content publishing workflow
- Hotel procurement knowledge base
- Supplier and product database structure
- Google Drive document organization
- Google Sheets procurement trackers
- Claude prompt library for business planning and document work
- Codex prompt library for repository, automation, and code tasks
- GitHub-based version control and change tracking
- n8n workflow automation for sourcing, documents, and operations
- Internal templates for PI, CI, RFQ, and procurement documentation

## AI Nightly Workflow System

The repository now includes a draft-only nightly AI workflow layer under `automation/`.

Start here:

- `automation/README.md` explains the architecture, folder structure, safety rules, n8n import steps, manual review process, rollback, and troubleshooting.
- `automation/n8n/nightly-ai-workflow.json` is the n8n workflow import file.
- `automation/prompts/` contains the AI prompts for classification, privacy redaction, supplier extraction, hotel procurement extraction, website drafts, social posts, and daily reports.
- `data/schemas/` contains Google Sheets / Notion / CSV-compatible schemas.

Automation must only create draft or pending-review outputs. It must not publish website changes without human approval.

## Platform Strategy

### Google Drive

Google Drive will be used for business file storage, shared documents, supplier records, and operational collaboration.

### Claude

Claude will support business writing, supplier communication, procurement analysis, document drafting, and planning workflows.

### Codex

Codex will support repository maintenance, website development, automation scripts, documentation structure, and technical implementation.

### GitHub

GitHub will provide version control, repository history, collaboration, issue tracking, and the foundation for future deployment workflows.

### Cloudflare Pages

Cloudflare Pages is planned as a future hosting option for the company website. No website is being built in this initialization step.

### Google Sheets

Google Sheets will support structured tracking for suppliers, products, quotations, purchase records, and hotel procurement comparisons.

### n8n

n8n will be considered for workflow automation across documents, notifications, procurement tracking, and AI-assisted operations.

---

# XRM GLOBAL TRADE LIMITED

## 公司简介

XRM GLOBAL TRADE LIMITED 正在建立一个系统化的数字化工作空间，用于支持国际贸易、跨境采购、酒店供应链管理、商务文件管理以及 AI 辅助运营。

本仓库是公司的官方长期工作空间，将用于承载公司网站基础、采购知识库、自动化脚本、业务文档以及可复用的 AI 提示词。

## 业务范围

XRM GLOBAL TRADE LIMITED 致力于连接国际买家与中国供应链资源，提供采购、寻源、文件整理及贸易执行支持。

主要方向包括：

- 中国供应链
- 酒店 FF&E
- 酒店 OS&E
- 跨境采购
- 国际贸易
- 供应商与产品调研
- 商务文件准备
- AI 辅助工作流自动化

## 中国供应链

本仓库将用于整理与中国供应链相关的知识、供应商记录、产品分类、模板和操作流程。

## 酒店 FF&E

酒店 FF&E 采购资料将归档在采购知识库中，包括产品类别、供应商资料、规格要求、报价流程和项目文件。

## 酒店 OS&E

酒店 OS&E 资源将支持酒店运营用品及设备的标准化采购流程，包括供应商比较、产品清单和询价资料。

## 跨境采购

本工作空间将支持跨境采购流程，包括供应商寻源、报价管理、发票文件、采购协调、物流参考和质量控制记录。

## 国际贸易

国际贸易相关文件、商业模板、采购记录和运营知识将长期维护在本仓库中，供公司持续使用。

## 仓库结构

```text
website/
  pages/
  assets/
    images/
    css/
    js/

blog/

docs/
  PI/
  CI/
  RFQ/
  Templates/

procurement/
  Hotel/
  Suppliers/
  Products/

knowledge-base/

automation/
  scripts/

prompts/
  Claude/
  Codex/
```

## 未来路线图

计划建设方向包括：

- 公司网站内容与 Cloudflare Pages 部署
- 博客与公司内容发布流程
- 酒店采购知识库
- 供应商与产品数据库结构
- Google Drive 文件组织
- Google Sheets 采购追踪表
- Claude 提示词库，用于商务规划和文件写作
- Codex 提示词库，用于仓库、自动化和代码任务
- GitHub 版本控制与变更记录
- n8n 自动化工作流，用于寻源、文件和运营流程
- PI、CI、RFQ 及采购文件内部模板

## AI 夜间自动工作流系统

本仓库已经加入只生成草稿的夜间 AI 自动工作流层，位置在 `automation/`。

请从这里开始：

- `automation/README.md` 说明系统架构、文件夹结构、安全规则、n8n 导入方式、人工审核流程、回滚方式和排错方法。
- `automation/n8n/nightly-ai-workflow.json` 是可导入 n8n 的工作流文件。
- `automation/prompts/` 保存文件分类、隐私脱敏、供应商提取、酒店采购提取、网站草稿、社媒文案、日报生成提示词。
- `data/schemas/` 保存兼容 Google Sheets / Notion / CSV 的字段结构。

自动化只能生成 draft 或 pending-review 内容，不允许在没有人工审核的情况下公开发布网站更新。

## 平台策略

### Google Drive

Google Drive 将用于商务文件存储、共享文档、供应商资料和运营协作。

### Claude

Claude 将支持商务写作、供应商沟通、采购分析、文件起草和规划流程。

### Codex

Codex 将支持仓库维护、网站开发、自动化脚本、文档结构和技术实现。

### GitHub

GitHub 将用于版本控制、历史记录、协作、问题追踪，并作为未来部署流程的基础。

### Cloudflare Pages

Cloudflare Pages 计划作为未来公司网站的托管方案。本次初始化不会构建网站。

### Google Sheets

Google Sheets 将用于供应商、产品、报价、采购记录和酒店采购比较的结构化追踪。

### n8n

n8n 将用于探索文件、通知、采购追踪和 AI 辅助运营等自动化工作流。

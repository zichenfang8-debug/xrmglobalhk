# 03_CONTENT — 内容生产线

## 用途
XRM 所有对外内容的生产和存档中心：SEO 文章、网站文案、社媒内容。
统一管理内容从草稿到发布的完整生命周期。

## 子目录

| 目录 | 用途 |
|------|------|
| `seo-articles/` | 已发布的 SEO 文章存档（英文） |
| `website-copy/` | 网站页面文案（英文） |
| `social-posts/` | LinkedIn / 社媒内容（中英文） |
| `_drafts/` | 所有待发布内容的草稿区 |

## 内容工作流
```
_drafts/ (撰写/AI生成)
    ↓ 审核通过
seo-articles/ | website-copy/ | social-posts/ (发布归档)
```

## 语言规范
- SEO 内容：**英文**（面向国际客户）
- 市场报告：**中文**（内部研究，存入 04_INTELLIGENCE/）
- 社媒内容：中英文双语

## 文件命名
```
YYYY-MM-DD-[主题关键词]-[语言].md
例：2026-07-01-china-hotel-ffe-supplier-guide-en.md
例：2026-07-01-ai-data-center-procurement-en.md
```

## SEO 文章要求
- 目标关键词放在文件名和 H1 中
- 字数：1500-3000 词
- 包含 meta description（文章顶部注释区）
- 内链指向 XRM 服务页面

## AI 更新规则
- AI 生成内容先进入 `_drafts/`，人工审核后移入对应目录
- 每篇文章发布后，在文章顶部注释中记录发布日期和 URL

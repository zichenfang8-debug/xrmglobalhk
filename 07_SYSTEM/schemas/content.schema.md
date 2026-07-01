# Schema: SEO 内容库 / 网站内容

**版本**: v1.0
**创建**: 2026-07-01
**对应目录**: `03_CONTENT/`

---

## 文章头部元数据（Frontmatter）

每篇 Markdown 内容文件顶部必须包含以下注释块：

```markdown
<!--
title: [文章标题]
slug: [URL-friendly-slug]
category: seo-article | website-copy | social-post | blog
language: en | zh | bilingual
target_keywords: ["keyword1", "keyword2"]
target_audience: hotel-developer | procurement-manager | epc-contractor | general
word_count: 0
status: draft | review | published | archived
published_url: 
published_date: YYYY-MM-DD
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
generated_by: ai | human | ai-assisted
reviewed_by: 
-->
```

---

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 文章标题（含目标关键词） |
| `slug` | ✅ | URL 路径，全小写，连字符分隔 |
| `category` | ✅ | 内容类型 |
| `language` | ✅ | 语言 |
| `target_keywords` | ✅ | 目标 SEO 关键词列表（至少1个） |
| `target_audience` | ✅ | 目标读者 |
| `word_count` | ✅ | 发布前更新 |
| `status` | ✅ | 工作流状态 |
| `published_url` | ❌ | 发布后填入完整 URL |
| `published_date` | ❌ | 发布日期 |
| `generated_by` | ✅ | 生成方式标记 |
| `reviewed_by` | ❌ | 审核人 |

---

## SEO 文章结构规范

```markdown
# [H1：含主关键词]

[Lead paragraph: 2-3 sentences, contains primary keyword]

## [H2: Secondary keyword or topic]
[300-500 words]

## [H2: Another topic]
[300-500 words]

## Conclusion
[50-100 words + CTA]
```

---

## 变更历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-07-01 | 初始创建 |

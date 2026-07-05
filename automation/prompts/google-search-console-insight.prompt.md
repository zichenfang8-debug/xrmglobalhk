# Google Search Console Insight Prompt

## Role

Analyze Google Search Console performance data and create SEO action items for XRM Global HK.

## Input

```json
{
  "date_range": "",
  "rows": [
    {
      "query": "",
      "page": "",
      "country": "",
      "device": "",
      "clicks": 0,
      "impressions": 0,
      "ctr": 0,
      "position": 0
    }
  ]
}
```

## Output

Return:

- Top opportunities
- Pages needing title/meta improvement
- Queries needing new content
- Internal link recommendations
- Draft blog briefs
- Manual review checklist

## Rules

- Do not modify live pages.
- Do not invent analytics data.
- Mark small-sample findings as `Low confidence`.

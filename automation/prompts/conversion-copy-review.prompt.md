# Conversion Copy Review Prompt

## Role

Review website copy for clarity, trust, and RFQ conversion.

## Input

```json
{
  "page_name": "",
  "page_text": "",
  "target_buyer": "",
  "desired_action": "RFQ inquiry"
}
```

## Output

Return:

- Clarity issues
- Trust gaps
- CTA improvements
- Suggested headline
- Suggested section edits
- Confidentiality risks
- Manual review checklist

## Rules

- Keep public-facing output in English.
- Do not use exaggerated claims.
- Do not name confidential clients or projects.
- Do not overwrite existing page copy. Produce draft recommendations only.

# Supplier Comparison Prompt

## Role

Create a reviewable supplier comparison from normalized RFQ and quotation data.

## Input

```json
{
  "rfq_id": "",
  "line_items": [],
  "suppliers": [],
  "quotes": []
}
```

## Output

Return:

- Supplier comparison table
- Best-fit supplier shortlist
- Price and lead-time summary
- Missing data list
- Risk notes
- Questions for suppliers
- Manual review checklist

## Rules

- Do not choose a final supplier automatically.
- Do not send messages automatically.
- Do not expose confidential buyer or project information.
- Use `Needs verification` where data is incomplete.

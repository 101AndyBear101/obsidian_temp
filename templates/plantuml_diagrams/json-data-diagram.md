---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/json-data
---

# JSON Data Diagram

## Purpose

Use to render JSON data as a readable structural diagram.

## Diagram

```plantuml
@startjson
{
  "service": "example",
  "enabled": true,
  "ports": [80, 443]
}
@endjson
```

## Explanation

- **Keys**: Property names in the JSON structure.
- **Values**: The data values for each property.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] The JSON is syntactically valid.
- [ ] Nested structures are clearly readable.
- [ ] No sensitive or private information is included.

## Related

-

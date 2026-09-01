---
kind: resource
project:
  - homelab-documentation-baseline
status: active
created: 2026-08-25
tags: []
---

# Homelab Operations Reference

## Purpose

Collect reusable standards and procedures for documenting, protecting, and recovering a fictional homelab environment.

## Key Information

- [[notes/homelab-inventory-standard|Homelab inventory standard]] defines the minimum safe inventory record.
- [[notes/homelab-backup-verification|Homelab backup verification]] defines how to test recoverability.
- [[notes/homelab-overview|Homelab overview]] assembles both topics for an operator.

## Related Notes

```base
views:
  - type: table
    name: Related notes
    filters:
      and:
        - file.inFolder("notes")
        - kind == "note"
        - resource.contains("homelab-operations-reference")
        - status != "archive"
    order:
      - file.name
      - type
      - status
      - file.mtime
```

## Related

- [[projects/homelab-documentation-baseline|Homelab documentation baseline]]
- [[areas/homelab|Homelab area]]

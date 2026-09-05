---
kind: resource
project:
  - personal
status: active
created: 2026-09-02
tags:
  - personal
---
# Personal Resource

## Purpose

Describe the reference material, source, or body of knowledge this resource collects.

## Key Information

- Project: [[projects/personal|Personal]]

## Related Notes

```base
views:
  - type: table
    name: Related notes
    filters:
      and:
        - kind == "note"
        - resource.contains("personal")
    order:
      - file.name
      - type
      - status
      - file.mtime

```

---
kind: area
status: active
created: 2026-09-02
tags:
  - personal
---
# Personal

## Purpose

Describe the ongoing responsibility this area represents and what healthy maintenance looks like.

## Standards

- [ ] Add the standards, recurring responsibilities, or boundaries for this area.

## Active Projects

```base
views:
  - type: table
    name: Active projects
    filters:
      and:
        - kind == "project"
        - area == "personal"
    order:
      - file.name
      - status
      - file.mtime

```

## Related

- [[projects/personal|Personal project]]

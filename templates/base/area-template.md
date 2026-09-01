---
kind: area
status: active
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: []
---

# area-name

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
        - file.inFolder("projects")
        - kind == "project"
        - area == "area-name"
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

## Related

-

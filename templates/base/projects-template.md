---
kind: project
area: project-area
status: active
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: []
---

# project-name

## Goal

Define the finite outcome and why it matters.

## Current State

Summarize progress, constraints, and the current blocker if there is one.

## Next Actions

- [ ]

## Notes and Decisions

-

## Resources

```base
views:
  - type: table
    name: Project resources
    filters:
      and:
        - file.inFolder("resources")
        - kind == "resource"
        - project.contains("project-name")
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

## Completion Criteria

- [ ]

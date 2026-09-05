---
kind: project
area: project-area
status: active
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: []
---
# Title

## Overview

Define the finite outcome and why it matters.

## Status

Summarize progress, constraints, and the current blocker if there is one.

## Actions

- [ ]

## Notes

-

## Related Items

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

## Completion

- [ ]

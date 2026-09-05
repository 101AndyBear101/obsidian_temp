---
kind: project
area: personal
status: active
created: 2026-09-02
tags:
  - personal
---

# Personal

## Goal

Define the finite outcome and why it matters.

## Current State

Summarize progress, constraints, and the current blocker if there is one.

## Next Actions

- [ ]

## Notes and Decisions

- Area: [[areas/personal|Personal]]

## Resources

- [[resources/personal|Personal Resource]]

```base
views:
  - type: table
    name: Project resources
    filters:
      and:
        - kind == "resource"
        - project.contains("personal")
    order:
      - file.name
      - status
      - file.mtime

```

## Completion

- [ ]

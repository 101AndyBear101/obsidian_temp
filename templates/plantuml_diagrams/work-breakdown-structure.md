---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/wbs
---
# Work Breakdown Structure

## Purpose

Use to break a project into progressively smaller work items.

## Diagram

```plantuml
@startwbs
* Project
** Planning
*** Define scope
** Delivery
*** Build
*** Review
@endwbs
```

## Explanation

- **Root**: The project being decomposed.
- **Level 1 branches**: Major phases or workstreams.
- **Level 2 branches**: Specific work packages or deliverables.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Each level represents a progressively detailed breakdown.
- [ ] Branch labels describe concrete deliverables or work items.
- [ ] No sensitive or private information is included.

## Related

-

---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - mermaid
  - diagram/gantt
---
# Project Gantt Plan

## Purpose

Use to lay out sequential work, dependencies, and milestones on a calendar.

## Diagram

```mermaid
gantt
  title Service rollout
  dateFormat YYYY-MM-DD
  section Plan
    Document requirements :done, requirements, 2026-08-24, 2d
    Prepare host :prepare, after requirements, 2d
  section Deploy
    Deploy service :deploy, after prepare, 1d
    Verify service :milestone, after deploy, 0d
```

## Explanation

- **Sections**: Workstreams or phases in the project.
- **Tasks**: Named bars with start dates and durations.
- **Milestones**: Zero-duration markers for key events.
- **Dependencies**: Task sequencing via "after" relationships.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Task names clearly indicate the work item.
- [ ] Dates and durations are realistic for the plan.
- [ ] Milestones represent verifiable events.
- [ ] No sensitive or private information is included.

## Related

-

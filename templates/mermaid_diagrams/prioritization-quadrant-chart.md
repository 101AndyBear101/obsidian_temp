---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - mermaid
  - diagram/quadrant
---

# Priority Quadrant

## Purpose

Use to compare work items across two decision criteria.

## Diagram

```mermaid
quadrantChart
  title Service priorities
  x-axis Low effort --> High effort
  y-axis Low impact --> High impact
  quadrant-1 Plan
  quadrant-2 Do next
  quadrant-3 Defer
  quadrant-4 Delegate
  Backup automation: [0.35, 0.8]
  Dashboard refresh: [0.7, 0.45]
```

## Explanation

- **Quadrants**: Priority categories defined by two axes.
- **Items**: Work items plotted by their coordinates on the axes.
- **Axes**: Decision criteria (e.g. effort vs impact).

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Quadrant labels clearly communicate each category.
- [ ] Items are placed in the correct quadrant for their priority.
- [ ] No sensitive or private information is included.

## Related

-

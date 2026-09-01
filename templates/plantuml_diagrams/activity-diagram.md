---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/activity
---

# Activity Diagram

## Purpose

Use to describe a workflow with actions, decisions, and outcomes.

## Diagram

```plantuml
@startuml
start
:Receive request;
if (Valid?) then (yes)
  :Process request;
else (no)
  :Return error;
endif
stop
@enduml
```

## Explanation

- **Start/Stop**: Workflow entry and termination.
- **Actions**: Steps in the process.
- **Decisions**: Branch points with labeled outcomes.
- **Arrows**: Flow direction between actions.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Every path from start reaches a stop node.
- [ ] Decision branches cover all expected outcomes.
- [ ] Labels are descriptive without the source file.
- [ ] No sensitive or private information is included.

## Related

-

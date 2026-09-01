---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/state
---

# State Diagram

## Purpose

Use to show valid states and the events that transition between them.

## Diagram

```plantuml
@startuml
[*] --> Stopped
Stopped --> Starting: start
Starting --> Running: ready
Running --> Stopped: stop
Running --> Failed: error
Failed --> Stopped: reset
@enduml
```

## Explanation

- **States**: Named conditions an entity can be in.
- **[*]**: Initial and terminal pseudo-states.
- **Transitions**: Events that cause a state change.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Every state is reachable from the initial state.
- [ ] Transition events describe meaningful triggers.
- [ ] No sensitive or private information is included.

## Related

-

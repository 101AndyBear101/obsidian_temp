---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/component
---

# Component Diagram

## Purpose

Use to show software components and the interfaces or protocols between them.

## Diagram

```plantuml
@startuml
left to right direction
component "Client" as client
component "API" as api
database "Database" as db

client --> api: HTTPS
api --> db: SQL
@enduml
```

## Explanation

- **Components**: Software modules or services.
- **Interfaces/Protocols**: The communication method between components.
- **Dependencies**: Lines showing directional usage relationships.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] All component dependencies are clearly annotated.
- [ ] Direction arrows show the correct data or call flow.
- [ ] No sensitive or private information is included.

## Related

-

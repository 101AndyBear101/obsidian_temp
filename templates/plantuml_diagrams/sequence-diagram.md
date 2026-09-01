---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/sequence
---

# Sequence Diagram

## Purpose

Use to show messages and responses between people, services, or systems over time.

## Diagram

```plantuml
@startuml
actor User
participant "Service" as Service
database Database as DB

User -> Service: Request
activate Service
Service -> DB: Query
DB --> Service: Result
Service --> User: Response
deactivate Service
@enduml
```

## Explanation

- **Participants**: People, services, or systems exchanging messages.
- **Activation bars**: Period during which a participant is active.
- **Solid arrows**: Direct calls or requests.
- **Dashed arrows**: Responses or returns.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] All messages have a sender and receiver.
- [ ] Activation and deactivation match request/response pairs.
- [ ] The sequence follows a logical temporal order.
- [ ] No sensitive or private information is included.

## Related

-

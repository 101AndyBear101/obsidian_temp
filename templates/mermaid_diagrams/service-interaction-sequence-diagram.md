---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - mermaid
  - diagram/sequence
---

# Service Interaction Sequence

## Purpose

Use to show messages exchanged between a person, service, and dependency over time.

## Diagram

```mermaid
sequenceDiagram
  actor User
  participant App as Application
  participant DB as Database
  User->>App: Submit request
  App->>DB: Read data
  DB-->>App: Return data
  App-->>User: Show result
```

## Explanation

- **Actors/Participants**: People, services, or components exchanging messages.
- **Arrows**: Messages sent between participants.
- **Solid arrows**: Direct calls or requests.
- **Dashed arrows**: Responses or returns.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] All messages have a sender and receiver.
- [ ] The sequence follows a logical temporal order.
- [ ] Responses match their corresponding requests.
- [ ] No sensitive or private information is included.

## Related

-

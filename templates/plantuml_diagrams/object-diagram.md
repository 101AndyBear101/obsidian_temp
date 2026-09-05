---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/object
---
# Object Diagram

## Purpose

Use to show a concrete snapshot of objects and their current values.

## Diagram

```plantuml
@startuml
object "service: Service" as service {
  state = running
  port = 8080
}

object "config: Configuration" as config {
  host = example.local
}

service --> config : reads
@enduml
```

## Explanation

- **Objects**: Concrete instances with their current state values.
- **Fields**: The attributes and their runtime values.
- **Links**: Relationships between instances.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Object names include their type in the format "name: Type".
- [ ] State values are realistic examples.
- [ ] No sensitive or private information is included.

## Related

-

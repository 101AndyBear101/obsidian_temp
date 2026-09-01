---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/deployment
---

# Deployment Diagram

## Purpose

Use to map applications and services onto hosts, VMs, containers, or devices.

## Diagram

```plantuml
@startuml
node "Host" as host {
  node "Container" as container {
    component "Application" as app
  }
}
database "Database" as db

app --> db: TCP
@enduml
```

## Explanation

- **Nodes**: Physical or virtual hosts.
- **Containers**: Runtime environments within a host.
- **Components**: Applications deployed inside containers.
- **Databases**: Persistent storage systems.
- **Connections**: Communication protocols between elements.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Hosting hierarchy (node > container > component) is logical.
- [ ] Communication protocols are specified.
- [ ] No sensitive or private information is included.

## Related

-

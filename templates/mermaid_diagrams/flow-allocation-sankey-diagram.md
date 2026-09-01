---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - mermaid
  - diagram/sankey
---

# Flow Allocation Sankey Diagram

## Purpose

Use to visualize quantities transferred between stages or categories.

## Diagram

```mermaid
sankey-beta
Internet,Firewall,100
Firewall,Services,80
Firewall,Blocked,20
Services,Application,60
Services,Monitoring,20
```

## Explanation

- **Nodes**: Stages or categories in the flow (e.g. Internet, Firewall).
- **Links**: Quantities flowing between nodes.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] All nodes have at least one input or output link.
- [ ] Quantities are realistic and roughly balanced.
- [ ] Labels are descriptive without the source file.
- [ ] No sensitive or private information is included.

## Related

-

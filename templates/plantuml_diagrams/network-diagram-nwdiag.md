---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - plantuml
  - diagram/network
---

# Network Diagram (nwdiag)

## Purpose

Use to document network segments, addresses, and the devices attached to them.

## Diagram

```plantuml
@startnwdiag
nwdiag {
  network lan {
    address = "10.0.0.0/24";
    client [address = "10.0.0.10"];
    server [address = "10.0.0.20"];
  }
}
@endnwdiag
```

## Explanation

- **Networks**: Logical or physical network segments with subnet addresses.
- **Devices**: Hosts, clients, or servers attached to a network.
- **Addresses**: IP addresses assigned to each device.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Network addresses use valid CIDR notation.
- [ ] Device addresses fall within their assigned network range.
- [ ] No sensitive or private information is included.

## Related

-

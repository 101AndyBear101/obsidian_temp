---
kind: note
resource:
  - homelab-operations-reference
status: active
type: permanent
created: 2026-08-25
tags:
  - homelab/documentation
---

# Homelab Inventory Standard

## Purpose

Define the minimum information needed to understand a homelab component without recording credentials, live addresses, or private identifiers.

## Inventory Standard

Record one entry per component with these fields:

| Field | Example |
| --- | --- |
| Role | Virtualization host |
| Platform | `<platform-name>` |
| Location | `<logical-location>` |
| Management method | Web console and secure shell |
| Configuration source | `<configuration-note>` |
| Backup method | `<backup-method>` |
| Recovery dependency | `<required-service-or-file>` |
| Owner or area | `homelab` |

Use placeholders in the reusable template. Store secrets in an approved secret manager, never in the vault.

## Validation

An inventory entry is complete when another reader can identify the component's purpose, find its canonical configuration note, and locate its recovery procedure without needing a credential from this vault.

## Related

- [[resources/homelab-operations-reference|Homelab operations reference]]
- [[projects/homelab-documentation-baseline|Homelab documentation baseline]]
- [[notes/homelab-overview|Homelab overview]]

---
kind: area
status: active
created: 2026-08-25
tags: []
---

# Homelab

## Purpose

Maintain a safe, reliable learning environment for experimenting with infrastructure, documentation, backup, and recovery practices. Healthy maintenance means the environment can be understood and restored from the vault without storing live credentials or private configuration.

## Standards

- Document material changes in canonical notes.
- Use placeholders for addresses, credentials, and environment-specific identifiers.
- Verify backups with a test restore on a regular schedule.
- Keep projects finite; move enduring responsibilities back into this area.
- Archive superseded guidance instead of deleting useful history.

## Active Projects

```base
views:
  - type: table
    name: Active projects
    filters:
      and:
        - file.inFolder("projects")
        - kind == "project"
        - area == "homelab"
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

## Related

- [[projects/homelab-documentation-baseline|Homelab documentation baseline]]
- [[projects/homelab-wiki-launch|Homelab wiki launch]]
- [[notes/homelab-overview|Homelab overview]]

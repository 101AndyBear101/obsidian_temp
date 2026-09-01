---
kind: project
area: homelab
status: active
created: 2026-08-25
tags: []
---

# Homelab Documentation Baseline

## Goal

Create a reusable baseline that explains what belongs in a homelab inventory and how backup recovery is verified, without exposing live infrastructure details.

## Current State

The [[areas/homelab|homelab area]] and [[resources/homelab-operations-reference|homelab operations resource]] are connected. [[notes/homelab-inventory-standard|The inventory standard]], [[notes/homelab-backup-verification|backup verification procedure]], and [[notes/homelab-overview|contextual overview]] demonstrate how canonical procedures are assembled for day-to-day use.

## Next Actions

- [x] Define [[notes/homelab-inventory-standard|a privacy-safe inventory standard]].
- [x] Define [[notes/homelab-backup-verification|a backup verification procedure]].
- [x] Assemble the procedures in [[notes/homelab-overview|a contextual overview]].
- [ ] Replace fictional placeholders only after copying the template vault for personal use.

## Notes and Decisions

- Relationships use plain lowercase-kebab-case filenames in metadata for reliable Base queries.
- Canonical procedures remain in `notes/`; this project note tracks the finite outcome.

## Resources

```base
views:
  - type: table
    name: Project resources
    filters:
      and:
        - file.inFolder("resources")
        - kind == "resource"
        - project.contains("homelab-documentation-baseline")
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

## Completion Criteria

- [x] The homelab operations resource appears in this project's resource view.
- [x] The related atomic notes appear in the resource's note view.
- [x] The overview embeds canonical headings without copying their content.

## Related

- [[areas/homelab|Homelab area]]
- [[resources/homelab-operations-reference|Homelab operations reference]]
- [[notes/homelab-overview|Homelab overview]]

---
kind: resource
project:
  - homelab-wiki-launch
status: active
created: 2026-08-25
tags: []
---

# Wiki Authoring Reference

## Purpose

Collect reusable guidance for writing, reviewing, and publishing contextual wiki pages from canonical notes.

## Key Information

- [[notes/wiki-content-standard|Wiki content standard]] defines the expected page structure.
- [[notes/wiki-publishing-workflow|Wiki publishing workflow]] defines the review and publishing sequence.
- [[notes/wiki-overview|Wiki overview]] demonstrates a contextual landing page.

## Related Notes

```base
views:
  - type: table
    name: Related notes
    filters:
      and:
        - file.inFolder("notes")
        - kind == "note"
        - resource.contains("wiki-authoring-reference")
        - status != "archive"
    order:
      - file.name
      - type
      - status
      - file.mtime
```

## Related

- [[projects/homelab-wiki-launch|Homelab wiki launch]]
- [[areas/homelab|Homelab area]]

---
kind: project
area: homelab
status: active
created: 2026-08-25
tags: []
---

# Homelab Wiki Launch

## Goal

Define and demonstrate a small publishing workflow that turns canonical source notes into a navigable homelab wiki.

## Current State

The [[resources/wiki-authoring-reference|wiki authoring resource]] now connects [[notes/wiki-content-standard|the content standard]] and [[notes/wiki-publishing-workflow|publishing workflow]]. [[notes/wiki-overview|The contextual overview]] embeds both canonical sections as an example landing page.

## Next Actions

- [x] Define [[notes/wiki-content-standard|the structure of a durable wiki page]].
- [x] Document [[notes/wiki-publishing-workflow|the review and publishing workflow]].
- [x] Assemble [[notes/wiki-overview|a contextual wiki overview]].
- [ ] Add new topic pages only when they have a clear audience or operational use.

## Notes and Decisions

- Wiki pages provide context; atomic notes remain the canonical source of reusable instructions.
- Path-qualified links are used when filenames repeat across folders.

## Resources

```base
views:
  - type: table
    name: Project resources
    filters:
      and:
        - file.inFolder("resources")
        - kind == "resource"
        - project.contains("homelab-wiki-launch")
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

## Completion Criteria

- [x] The wiki authoring resource appears in this project's resource view.
- [x] Its atomic notes appear in the resource's related-note view.
- [x] The overview renders the canonical sections through embeds.

## Related

- [[areas/homelab|Homelab area]]
- [[resources/wiki-authoring-reference|Wiki authoring reference]]
- [[notes/wiki-overview|Wiki overview]]

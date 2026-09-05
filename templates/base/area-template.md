---
kind: area
status: active
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: []
---
# Title

## Overview
```internal_prompt
1. Define the ongoing responsibility or life domain this area owns.
2. Describe the kinds of work, decisions, and topics that belong in it.
3. State the long-term outcome this area should maintain.

Use the area name as the subject. An area is ongoing, not a finite project.
```
## Guidelines
```internal_prompt
1. List the recurring responsibilities needed to maintain this area.
2. Define the standards or principles that guide work in this area.
3. State what does not belong in this area and should be routed elsewhere.

Keep the guidance practical and stable; do not add temporary project tasks here.
```

## Related Items
```internal_prompt
1. Identify the kinds of finite projects this area is expected to contain.
2. Decide whether the Base view should list projects associated with this area automatically.
3. If projects should not be listed automatically, provide concise manual relationship context instead.

If the projects should be listed automatically, replace `area-name` in the Base filter below with the area note's filename without `.md`.
```

```base
views:
  - type: table
    name: Active projects
    filters:
      and:
        - file.inFolder("projects")
        - kind == "project"
        - area == "area-name"
        - status != "archive"
    order:
      - file.name
      - status
      - file.mtime
```

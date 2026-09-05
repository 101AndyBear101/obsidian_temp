---
kind: resource
project: []
status: active
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: []
---
# Title

## Overview

Describe the reference material, source, or body of knowledge this resource collects.

## Content

-

## Related Items

```base
views:
  - type: table
    name: Related notes
    filters:
      and:
        - file.inFolder("notes")
        - kind == "note"
        - resource.contains("resource-name")
        - status != "archive"
    order:
      - file.name
      - type
      - status
      - file.mtime
```

---
kind: note
resource: []
status: active
type: diagram
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags:
  - diagram/generic
---
# Title

## Overview

Explain what this diagram shows and who benefits from it.

## Content

```mermaid
flowchart TD
  A[Start] --> B[End]
```

The default uses a `mermaid` fenced block. Use `plantuml` instead when its syntax is the better fit. See `templates/mermaid_diagrams/` and `templates/plantuml_diagrams/` for syntax and structure.

## Details

- **Element**: What it represents.

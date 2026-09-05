---
kind: note
resource: []
status: active
type: diagram
created: 2026-08-25
tags:
  - mermaid
  - diagram/requirement
---
# Requirement Traceability Diagram

## Purpose

Use to connect a requirement to the element that verifies it.

## Diagram

```mermaid
requirementDiagram
  requirement backup_requirement {
    id: R1
    text: "Backups complete successfully"
    risk: High
    verifymethod: Test
  }
  element backup_test {
    type: "test"
    docref: "Backup verification procedure"
  }
  backup_requirement - verifies -> backup_test
```

## Explanation

- **Requirements**: Named elements with ID, text, risk, and verification method.
- **Elements**: Components that verify or satisfy requirements.
- **Relationships**: Traceability links (e.g. "verifies") between requirements and elements.

## Validation

- [ ] The diagram renders without errors in Obsidian.
- [ ] Every requirement has a unique ID.
- [ ] All requirements trace to at least one verifying element.
- [ ] Risk levels are assigned where relevant.
- [ ] No sensitive or private information is included.

## Related

-

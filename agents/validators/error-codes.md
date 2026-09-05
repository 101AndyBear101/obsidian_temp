---
kind: guide
status: active
created: 2026-09-03
tags:
  - vault/validation
---

# Validation Issue Codes

Issue codes are stable within a validator. Explanations may become clearer without changing the code's meaning.

| Prefix  | Validator            | Codes                                                                                                                                                                                                                                          |
| ------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CFG`   | Configuration        | `CFG001` regenerated defaults                                                                                                                                                                                                                  |
| `LOG`   | Logging              | `LOG001` malformed historical JSON Lines record                                                                                                                                                                                                |
| `RUN`   | Execution            | `RUN001` validator could not run; `RUN002` no validation scripts discovered                                                                                                                                                                    |
| `META`  | Frontmatter          | `META001` invalid YAML; `META002` missing frontmatter; `META003` kind; `META004` status; `META005` date; `META006` missing recommended type; `META007` invalid type; `META008` required field; `META009` missing tags; `META010` tag data type |
| `REL`   | Relationships        | `REL001` missing recommendation; `REL002` data type; `REL003` identifier syntax; `REL004` identifier length                                                                                                                                    |
| `TAG`   | Tags                 | `TAG001` syntax; `TAG002` length                                                                                                                                                                                                               |
| `NAME`  | Naming               | `NAME001` daily-note format; `NAME002` daily-note date; `NAME003` general name                                                                                                                                                                 |
| `LINK`  | Wikilinks            | `LINK001` missing target; `LINK002` missing heading                                                                                                                                                                                            |
| `COV`   | Link coverage        | `COV001` no inbound link; `COV002` no outbound link                                                                                                                                                                                            |
| `ATT`   | Attachments          | `ATT001` missing embed; `ATT002` unreferenced attachment                                                                                                                                                                                       |
| `SEC`   | Sections             | `SEC001` recommended section                                                                                                                                                                                                                   |
| `IDX`   | Indexes              | `IDX001` index without wikilinks                                                                                                                                                                                                               |
| `TPL`   | Templates            | `TPL001` unclosed code fence                                                                                                                                                                                                                   |
| `SKILL` | Skills               | `SKILL002` missing skill file; `SKILL003` unregistered skill                                                                                                                                                                                   |
| `BASE`  | Bases                | `BASE001` missing folder; `BASE002` unsupported kind                                                                                                                                                                                           |
| `DUP`   | Duplicates           | `DUP001` similar filename                                                                                                                                                                                                                      |

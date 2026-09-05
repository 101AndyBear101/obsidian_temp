# Journals
```base
views:
  - type: cards
    name: Recent journals
    filters:
      and:
        - kind == "note"
        - type == "journal"
        - status != "archive"
    order:
      - file.name
      - resource
      - tags
    sort:
      - property: file.mtime
        direction: DESC
    limit: 3

```
# Notes
```base
views:
  - type: cards
    name: Recent notes
    filters:
      and:
        - kind == "note"
        - status != "archive"
    order:
      - file.name
      - resource
      - tags
    sort:
      - property: file.mtime
        direction: DESC
    limit: 6

```
# Resources
```base
views:
  - type: cards
    name: Active resources
    filters:
      and:
        - kind == "resource"
        - status != "archive"
    order:
      - file.name
      - project
    sort:
      - property: file.mtime
        direction: DESC

```
# Projects
```base
views:
  - type: cards
    name: Active projects
    filters:
      and:
        - kind == "project"
        - status != "archive"
    order:
      - file.name
      - area
    sort:
      - property: file.mtime
        direction: DESC

```
# Areas
```base
views:
  - type: cards
    name: Active areas
    filters:
      and:
        - kind == "area"
        - status != "archive"
    order:
      - file.name
    sort:
      - property: file.mtime
        direction: DESC

```

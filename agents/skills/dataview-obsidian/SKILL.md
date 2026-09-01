---
name: dataview-obsidian
description: Create and validate read-only Obsidian Dataview views; use for DQL or Dataview metadata queries, not Bases or generic Markdown tables.
status: active
tags:
  - skills/dataview-obsidian
---

# Obsidian Dataview

## Activation Boundary

Use this skill for the Obsidian Dataview community plugin: querying frontmatter or inline fields, writing `dataview` blocks, or evaluating Dataview expressions. Do not use it for Obsidian Bases, static Markdown tables, or ordinary notes without a Dataview query.

Before relying on query output, confirm that Dataview is installed and enabled. Inspect existing vault metadata conventions and query patterns; use available frontmatter and inline fields as data without inventing a new schema. Do not install, enable, or configure the plugin unless the user explicitly asks.

## DQL Views

Prefer narrow, readable DQL in `dataview` blocks for ordinary views. Constrain the source and result size to avoid broad, expensive queries:

````markdown
```dataview
TABLE status, created
FROM "projects"
WHERE status = "active"
SORT created DESC
LIMIT 20
```
````

Keep queries read-only by default. Use inline expressions only for small local values, such as `= this.status`, rather than turning an entire view into inline syntax. Validate output in Obsidian Live Preview or Reading View.

## JavaScript Boundary

Reserve `dataviewjs` blocks and inline JavaScript for requests that explicitly require JavaScript. Dataview JavaScript runs with plugin-level access and can create, edit, or delete files and make network calls. Do not add, run, or copy untrusted JavaScript without the user’s explicit authorization.

## Validation

1. Confirm referenced fields and source folders match existing vault conventions.
2. Verify the rendered query returns the intended, limited results in Live Preview or Reading View.
3. Confirm the query remains read-only unless the user expressly authorized JavaScript with its resulting permissions.

## Upstream Documentation

Use the [Dataview repository](https://github.com/blacksmithgu/obsidian-dataview) and [Dataview documentation](https://blacksmithgu.github.io/obsidian-dataview/) for advanced or version-sensitive syntax.

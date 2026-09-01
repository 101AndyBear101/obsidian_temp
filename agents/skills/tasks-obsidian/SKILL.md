---
name: tasks-obsidian
description: Author and query actionable tasks with the Obsidian Tasks community plugin; use for Tasks query blocks or plugin-specific task behavior, not generic checkboxes.
status: active
tags:
  - skills/tasks-obsidian
---

# Obsidian Tasks

## Activation Boundary

Use this skill when the user asks to create, query, organize, or update tasks with the Obsidian Tasks community plugin. Do not use it for ordinary Markdown checkboxes when no Tasks behavior, query, or plugin context is involved.

Before relying on Tasks behavior, confirm the plugin is installed and enabled and inspect the relevant plugin settings or existing vault conventions. Do not install, enable, or reconfigure the plugin unless the user explicitly asks.

## Author Tasks

Use standard task lines in source notes:

```markdown
- [ ] Confirm the deployment checklist
```

Keep task text specific and preserve the user's intended task state. Add Tasks-specific dates, recurrence, or other annotations only when the current plugin version and vault conventions support them. Use upstream documentation for version-sensitive syntax.

## Query Tasks

Place narrow `tasks` query blocks in the note that needs the task view. Scope by a meaningful property such as path, tag, or status, and limit output to keep the view useful:

````markdown
```tasks
not done
path includes projects/example-project
limit 20
```
````

Keep the result connected to its source: preserve the source-note context and verify that rendered query results link back to the task’s source note. Toggling a task in a query updates the source file, not the query note.

Request confirmation before applying mass task-state updates, especially across multiple source notes.

## Validation

1. Confirm the query and task lines render correctly in Obsidian Live Preview or Reading View.
2. Check that the query is narrow, limited, and returns the intended source-linked tasks.
3. After a state change through a query, verify the source note reflects the intended checkbox state.

## Upstream Documentation

Use the [Obsidian Tasks documentation](https://publish.obsidian.md/tasks/) and [upstream repository](https://github.com/obsidian-tasks-group/obsidian-tasks) for advanced or version-sensitive syntax.

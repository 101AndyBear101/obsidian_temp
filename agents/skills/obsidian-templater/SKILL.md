---
name: obsidian-templater
status: active
description: Create and troubleshoot Obsidian Templater templates and rules.
tags:
  - skills/obsidian-templater
---

# Obsidian Templater

## Vault Context

Templater is installed and active in this vault.

- Template folder: `templates/`
- Core Obsidian Templates folder: `templates/`
- No folder-template rules are currently configured.
- Existing base templates are under `templates/base/`.

Inspect `.obsidian/plugins/templater-obsidian/data.json` before changing plugin rules or relying on a setting.

## Use the Smallest Reliable Syntax

Use a standard command for a value inserted when the template runs:

```markdown
created: <% tp.file.creation_date("YYYY-MM-DD") %>
# <% tp.file.title %>
```

Use JavaScript execution only when control flow, a prompt/suggester, asynchronous work, or file APIs are genuinely needed:

```markdown
<%* const kind = await tp.system.suggester(["note", "project"], ["note", "project"]) %>
kind: <% kind %>
```

Execution blocks use `<%* ... %>`. They must `await` asynchronous Templater calls, including `tp.system.prompt()` and `tp.system.suggester()`.

Avoid dynamic commands (`<%+ ... %>`) for new templates: they resolve in preview mode, can be stale because of preview caching, and the official documentation notes they have known maintenance issues.

## Build a Template

1. Identify the note type and whether it is inserted into an existing note or creates a new note from a folder rule.
2. Start from the relevant vault template and preserve the metadata expected by Base views.
3. Use Templater only for values that must vary at creation time, such as title, date, prompt answers, or selected type.
4. Keep generated YAML valid after expansion. Quote values or use a YAML block scalar when the inserted value could contain YAML-sensitive characters.
5. Use `tp.file.cursor()` only where it improves capture flow; do not add cursors merely as decoration.
6. Test with a disposable note in the target folder and inspect the rendered Markdown, frontmatter, and Base-view behavior.

## File and Configuration Actions

`tp.file.create_new`, `tp.file.move`, and `tp.file.rename` change vault files. Use them only when the user explicitly asks for that behavior, make the target path clear, and avoid opening a newly created file before other asynchronous operations finish.

Do not enable or use Templater system commands, web functions, startup templates, or unreviewed user scripts without explicit approval. The plugin can execute arbitrary JavaScript and system commands; treat imported template code as untrusted until reviewed.

## Folder Template Rules

Before adding or changing a folder-template rule:

- Confirm the template path exists under `templates/`.
- Confirm the target folder and whether child folders should inherit it.
- Check for a deeper rule, because the most specific matching folder wins.
- Prefer a folder rule for stable note classes; use regex rules only when a folder cannot express the intent.
- Do not enable automatic triggering for unknown or unsafe newly created content.

## Troubleshooting Checklist

- Confirm the template is inside the configured template folder.
- Check Templater’s folder rule and the target file path.
- Verify command delimiters: `<% ... %>` for insertion and `<%* ... %>` for execution.
- Check function arguments are values, not documentation type annotations.
- Add `await` to asynchronous calls in execution blocks.
- Verify the generated frontmatter is valid YAML and the command is not inside an unintended code fence.

## Official References

- <https://silentvoid13.github.io/Templater/>
- <https://silentvoid13.github.io/Templater/syntax.html>
- <https://silentvoid13.github.io/Templater/settings.html>
- <https://silentvoid13.github.io/Templater/internal-functions/internal-modules/file-module.html>

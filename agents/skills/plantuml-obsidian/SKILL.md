---
name: plantuml-obsidian
status: active
description: Render PlantUML diagrams in Obsidian using the PlantUML plugin by joethei.
tags:
  - skills/plantuml-obsidian
---

# PlantUML for Obsidian

## Vault Context

The **PlantUML** community plugin (by joethei) renders PlantUML diagrams inside Obsidian notes. It uses the [PlantUML Online Server](https://plantuml.com/server) by default, or a local `.jar` file for offline rendering.

> [!important]
> Before changing plugin settings, inspect `.obsidian/plugins/obsidian-plantuml/` for its current configuration.
> Do not install, enable, or reconfigure the plugin unless the user explicitly asks.

## Usage

Create a fenced code block with `plantuml` as the language:

```markdown
```plantuml
Bob -> Alice : hello
Alice -> Wonderland : hello
@enduml
```
```

Three fenced block languages are supported:

| Language | Output |
| --- | --- |
| `plantuml` | PNG diagram |
| `plantuml-svg` | SVG diagram (higher resolution) |
| `plantuml-ascii` | ASCII art (sequence diagrams only) |

## Linking to Notes

PlantUML's web link syntax (`[[...]]`) conflicts with Obsidian wikilinks. Use **triple brackets** to link to vault notes:

```plantuml
[[[Your other note]]]
```

For the link target, use the same syntax as Obsidian internal links. Normal web links follow [PlantUML link syntax](https://plantuml.com/de/link).

## Including `.puml` Files

> Only works with local rendering (`.jar` file).

Use the standard PlantUML `!include` directive:

```plantuml
!include path/to/file.puml
```

## Rendering

The plugin renders diagrams via:

- **PlantUML Online Server** (default) — sends diagram source to `www.plantuml.com`
- **Local `.jar` file** — offline rendering, slower but private
- **Self-hosted server** — Docker, JEE, or PicoWeb instance

Treat internal hostnames, IP ranges, service names, and architecture details as potentially sensitive when using a remote renderer.

## Workflow

1. Choose the render method: online server, local `.jar`, or self-hosted server.
2. For sensitive diagrams, prefer local rendering or a self-hosted server.
3. Write the smallest diagram that communicates the needed structure.
4. Use `plantuml-svg` when higher resolution is needed.
5. Use `plantuml-ascii` only for sequence diagram ASCII art.
6. For reusable diagrams, extract the PlantUML source into `.puml` files and use `!include`.
7. Render in Obsidian and verify the output.

## Troubleshooting

- Confirm the fenced language is exactly `plantuml`, `plantuml-svg`, or `plantuml-ascii`.
- Check matching `@start...` / `@end...` directives.
- If rendering fails, verify the configured render method (server vs. local).
- ASCII output only supports sequence diagrams.
- For Chinese or non-Latin characters, switch to SVG rendering.
- The PicoWeb server does not support clickable links in PNG diagrams.

## Official Source

<https://github.com/joethei/obsidian-plantuml>
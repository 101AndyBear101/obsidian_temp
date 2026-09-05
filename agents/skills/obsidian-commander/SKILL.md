---
name: obsidian-commander
description: Configure Obsidian Commander commands in interface locations; use for command placement, visibility, ordering, and device-specific availability.
status: active
tags:
  - skills/obsidian-commander
---

# Obsidian Commander

## Outcome

Make requested Obsidian commands accessible in the intended interface location without changing unrelated command or plugin configuration.

## Activation Boundary

Use this skill for the Commander community plugin’s command placement, hiding, ordering, editing, or device-availability controls. Do not use it for creating new Obsidian commands, implementing a plugin, or changing generic hotkeys unless Commander configuration is explicitly in scope.

## Workflow

1. Confirm Commander is installed and enabled. Do not install, enable, or reconfigure it unless the user explicitly asks.
2. Identify the existing command, intended interface location, and whether it should be visible on every synced device.
3. Inspect the current Commander settings before changing them; preserve existing placements, hidden commands, and order outside the requested scope.
4. Apply the smallest requested placement, visibility, ordering, or device-targeting change.
5. If a command will be hidden, confirm an alternative way to invoke it when that could affect the user’s workflow.

## Validation

1. Confirm the command appears, is hidden, or is ordered as requested in the target interface.
2. Invoke the command from its new location and verify it performs the expected action.
3. Confirm unrelated interface locations and commands remain unchanged.

## Official Source

- <https://github.com/jsmorabito/obsidian-commander>

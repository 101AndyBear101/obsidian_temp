# Note Model Guidance

Use atomic source notes for canonical knowledge and contextual wiki notes to assemble that knowledge for a specific audience or task.

## Atomic Source Notes

- Keep one focused subject per note or per stable, self-contained heading.
- Store canonical configuration values, procedures, definitions, and decisions here.
- Use a stable `##` heading for content that other notes should embed.
- Name the note after its canonical subject, following [[naming-guidance|Vault Naming Guidance]].

Example:

```markdown
# Proxmox NFS Settings

## Mount Options

Canonical options and their explanation.
```

## Contextual Wiki Notes

- Use a host, service, or topic note to provide context and connect related material.
- Link or embed only the headings needed from atomic source notes.
- Do not copy canonical values into the wiki note; update the source note instead.

Example:

```markdown
## Storage

![[proxmox-nfs-settings#Mount Options]]
```

## Sensitive Content

- Never include credentials, tokens, private keys, personal details, or live network secrets.
- Replace sensitive examples with clear placeholders such as `<server-address>` or `<api-token>`.

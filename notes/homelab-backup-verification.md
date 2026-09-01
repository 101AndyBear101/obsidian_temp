---
kind: note
resource:
  - homelab-operations-reference
status: active
type: permanent
created: 2026-08-25
tags:
  - homelab/recovery
---

# Homelab Backup Verification

## Purpose

Provide a reusable procedure for demonstrating that a fictional homelab backup is readable and recoverable.

## Backup Verification Procedure

1. Select a recent backup from `<backup-target>` without modifying the source system.
2. Confirm the backup job reports a successful completion and expected retention date.
3. Restore the backup into an isolated test location named `<restore-test-location>`.
4. Verify the restored files or service start without relying on the original instance.
5. Compare a small set of expected records, files, or checksums.
6. Record the test date, result, and follow-up action in the applicable project or journal note.
7. Remove the disposable restore only after the result has been recorded.

> [!warning]
> A successful backup job is not proof of recovery. The validation requires an isolated restore test.

## Validation

The procedure passes when the restored sample is independently readable, expected content is present, and any exception has a documented owner and next action.

## Related

- [[resources/homelab-operations-reference|Homelab operations reference]]
- [[projects/homelab-documentation-baseline|Homelab documentation baseline]]
- [[notes/homelab-overview|Homelab overview]]

---
name: destill
description: >
  Delegate exact $craft:destill invocations to the canonical $craft:distill
  preview-and-confirm workflow for an existing repository-root SPEC.md.
---

# Destill alias

Skill metadata registers one name, so this alias delegates all behavior to
Distill. It has no independent rewrite, permission, or output contract.

1. Accept only the exact trimmed command `$craft:destill` with no arguments;
   otherwise return `INVALID_SCOPE` before repository inspection or writes.
2. Read all of `../distill/SKILL.md`.
3. Treat the accepted alias as exact `$craft:distill` and follow the canonical
   contract completely. Do not duplicate, weaken, or reinterpret its behavior.

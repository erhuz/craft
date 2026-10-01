---
name: destill
disable-model-invocation: true
description: >
  Delegate zero-argument $craft:destill or /craft:destill invocations, or desktop
  skill selection, to the canonical $craft:distill preview-and-confirm workflow
  for an existing repository-root SPEC.md.
---

# Destill alias

Before this workflow, read and apply `../_shared/entry.md`.

Skill metadata registers one name, so this alias delegates all behavior to
Distill. It has no independent rewrite, permission, or output contract.

1. Accept only the exact trimmed command `$craft:destill` or `/craft:destill`
   with no arguments, or the user's explicit selection of the installed
   Destill skill with no arguments. Otherwise return `INVALID_SCOPE` before
   repository inspection or writes.
2. Read all of `../distill/SKILL.md`.
3. Treat the accepted alias as exact `$craft:distill` and follow the canonical
   contract completely. Do not duplicate, weaken, or reinterpret its behavior.

---
name: destill
description: >
  Explicit compatibility alias for the canonical $craft:distill workflow. Use
  only when invoked exactly as $craft:destill to preview and confirm compaction
  of an existing repository-root SPEC.md. Skill metadata registers one name,
  so this separate selector only delegates; it contains no independent
  distillation behavior and changes no files outside the canonical contract.
---

# Destill alias

1. Accept only the exact trimmed command `$craft:destill` with no arguments;
   otherwise return `INVALID_SCOPE` before repository inspection or writes.
2. Read all of `../distill/SKILL.md`.
3. Treat the accepted alias as exact `$craft:distill` and follow the canonical
   contract completely. Do not duplicate, weaken, or reinterpret its behavior.

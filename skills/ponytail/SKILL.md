---
name: ponytail
disable-model-invocation: true
argument-hint: "[lite | full | ultra]"
description: >
  Choose the smallest correct solution under Craft's minimalism policy. Use
  $craft:ponytail or /craft:ponytail, or desktop skill selection, to select a
  mode; Build, Backprop, and Spec activate it on every run.
---

# Ponytail

Before applying this guidance, read and apply `../_shared/entry.md`.

Act as a lazy senior developer: efficient, not careless. Best code = code never
written. Applies to coding, design, review, refactoring, and implementation.

## Modes

| Mode | Behavior |
|------|----------|
| `lite` | Follow the requested approach; briefly suggest a simpler viable alternative when useful. |
| `full` | Apply the ladder and deliver the smallest correct implementation. |
| `ultra` | Challenge optional complexity before adding code; favor removing redundant parts within scope and reusing existing behavior. |

Select with `$craft:ponytail lite|full|ultra`; default `full`; a bare
invocation keeps the current mode. `stop ponytail` or `normal mode` suspends
this guidance until the next activation. Keep mode and suspension in
conversation context across turns, resume, and compaction.

An explicit `$craft:ponytail` or any Build, Backprop, or Spec run (including
delegated and resumed runs) activates Ponytail with the previous mode, a newly
supplied one, or `full`. When another skill activates it, continue that
workflow without acknowledging the mode. A SessionStart reload alone does not
reactivate it.

Modes and suspension never change explicit requirements, safety, verification,
or permission to enter another Craft phase. A mode-only or suspension request
gets a brief acknowledgement and starts no implementation.

## Use the ladder

First trace the affected flow and every place the change must reach: callers,
tests, fixtures, config, exports. Check what could break for users, including
data loss, exposure, and broken callers. Those updates are in scope; extra
features are not.

In `full` and `ultra`, stop at the first rung that holds; in `lite`, use it to
find alternatives:

1. Skip work with no current need.
2. Reuse what the codebase already has, following its established usage.
3. Use the standard library.
4. Use a native platform feature.
5. Use an already-installed dependency.
6. Use one line when one line is correct.
7. Write the minimum code that works.

Once a correct, simple solution is found, carry the task through required
verification; keep exploring only to resolve material uncertainty or finish
requested analysis. Between equally small solutions, pick the one that handles
edge cases with fewer assumptions. For bugs, fix the root cause once at the
shared ownership point, not with repeated symptom guards.

## Keep implementation small

- No speculative abstraction, dependency, configurability, or scaffolding.
- Prefer deletion over addition and boring code over clever code.
- Keep the codebase's layers, interfaces, conventions, and own components.
- Touch the fewest files that correctly own the behavior.
- Mark a deliberate simplification with a real ceiling using a `ponytail:`
  comment naming ceiling and upgrade trigger.
- For non-trivial logic, leave or reuse the smallest runnable check; add no
  test framework or broad fixtures for one behavior.

Never simplify away trust-boundary validation, data-loss prevention, security,
accessibility, required failure handling, or an explicit user requirement.

## Formulate like Ponytail

Interface copy follows Clarify. Lead with result or code; explain only what the
user asked for or needs to act. After implementation, use at most three short
lines: result, skipped complexity, and what would justify adding it. A more
specific skill output contract wins (Audit is issues-only; Caveman owns
`SPEC.md` encoding); requested reports and explanations keep their own form.

---
name: backprop
description: >
  Coordinate a confirmed defect from root-cause evidence into SPEC.md and a
  verified fix. Use only when explicitly invoked as $craft:backprop, or when
  $craft:build finds that the specification is missing, wrong, or allowed a
  failed behavior. Propose semantic changes, wait for confirmation, delegate
  them to $craft:spec, then delegate implementation and the combined commit to
  $craft:build. Do not mutate files directly.
---

# Backprop

Backprop is the defect-learning flow. It coordinates; Spec owns semantic
`SPEC.md` changes and Build owns code, tests, verification, status, staging, and
the commit.

## Do not backprop task-local mistakes

If an existing invariant or interface already requires the correct behavior and
an uncommitted implementation merely violates it, return the failure to Build
for correction. No new `§B` row is needed: the existing specification and gate
already caught the mistake before it became accepted behavior.

Backprop when a reported, shipped, previously accepted, or spec-permitted defect
reveals missing or wrong product knowledge.

## Resolve evidence

1. Resolve the current Git root and read only its `SPEC.md`.
2. If absent, return `SPEC_MISSING`, suggest `$craft:spec from-code`, and stop:
   no edits, tests, or speculative invariant.
3. Read the report or command failure, relevant code, tests, callers, state
   ownership, and local instructions.
4. Reproduce when safe and scoped, or name the exact evidence that establishes
   the failure.

## Trace

Name the root cause at its shared ownership point, not the visible symptom. Then
decide separately:

- `§V`: would a testable behavioral invariant have prevented recurrence?
- `§I`: is an interface, ownership boundary, side effect, or contract wrong?
- `§T`: is implementation work missing or was the wrong task built?

Every confirmed defect gets a `§B` row. Add `§V`, `§I`, or `§T` only when the
root cause requires it; an invariant is not mandatory for a one-time migration,
an external dependency failure, or a purely mechanical defect with no reusable
behavioral class.

## Propose and pause

Before any write, output:

```text
Cause: <root cause>
Evidence: <location or reproduction>
Spec proposal:
- §B row: <cause and resulting fix meaning>
- §V rule: <testable rule>              # only when needed
- §I contract: <interface change>       # only when needed
- §T task: <implementation task>        # only when needed
Regression: <failing test target or why no invariant/test applies>
```

Ask for confirmation of this semantic change set. Do not edit `SPEC.md`, tests,
or code before confirmation.

## Coordinate the confirmed fix

After confirmation:

1. Invoke `$craft:spec` with the confirmed change set. It allocates ledger IDs
   and applies semantic `SPEC.md` changes.
2. Invoke or resume `$craft:build` for the resulting task.
3. Build writes the named failing regression first when a new invariant exists,
   implements the smallest root-cause fix, and runs focused plus required final
   verification.
4. Build stages the exact spec, test, and code files and creates one combined
   commit: `fix: <root cause>`.

Return the applied SPEC diff, verification result, and commit without repeating
ledger identifiers in handoff prose. If verification exposes a different root
cause, stop and revise the proposal rather than recursively inventing more spec
history.

## Boundaries

- No direct file writes, status flips, tests, commits, or blind retries.
- No invariant from a symptom without root-cause evidence.
- No automatic confirmation of semantic product changes.
- No sub-agents, dashboards, or auxiliary history; `SPEC.md` and git are the
  record.

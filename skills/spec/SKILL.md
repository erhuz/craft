---
name: spec
description: >
  Create, distill, or amend the repository-root SPEC.md, and apply a confirmed
  backprop change set. Use only when explicitly invoked as $craft:spec for a new
  specification, from-code distillation, a targeted section amendment, or a
  semantic spec update proposed by $craft:backprop. This skill owns semantic
  SPEC.md content; it does not implement code, run builds, or commit.
---

# Spec

Own the meaning of `SPEC.md`. Build may change task status cells only. Backprop
may propose semantic changes but must route confirmed changes through this
skill.

## Resolve the ledger

1. Resolve the current Git root. If none exists, use the current directory.
2. Use only `<root>/SPEC.md`; never borrow a parent or sibling ledger.
3. Load exactly one format contract before inspecting or writing `SPEC.md`:
   read all of `<root>/FORMAT.md` when it exists; otherwise read all of
   `../caveman/SKILL.md` and use its SPEC format.
4. If the selected format contract is missing or unreadable, return
   `FORMAT_MISSING` and stop: no further repository inspection, SPEC write, or
   substitution from generic tools, model defaults, remembered syntax, or
   parent or sibling format files.
5. Read relevant local instructions before inspecting or changing files.

## Dispatch

- No `SPEC.md`, idea supplied: create a new spec.
- No `SPEC.md`, `from-code` supplied: distill the current codebase.
- Existing `SPEC.md`, `amend <section>` supplied: amend only that section and
  direct dependencies required to keep references valid.
- Confirmed Backprop change set supplied: apply it exactly, allocating final IDs.
- Raw bug or failed verification supplied: invoke `$craft:backprop`; do not turn
  an untraced symptom directly into an invariant.
- Missing or ambiguous input: ask one focused question and write nothing.

## Create

Turn the stated idea into:

1. `§G`: one outcome, not a feature inventory.
2. `§C`: current constraints and explicit non-goals.
3. `§I`: external interfaces, actors, data ownership, and side effects.
4. `§V`: testable behavioral invariants.
5. `§T`: the smallest ordered implementation tasks, all status `.`.
6. `§B`: an empty bug-history table.

Do not invent users, scale, integrations, configurability, or business rules.
Mark genuinely uncertain claims with `?`. Show the resulting diff. Never start
Build automatically.

## Distill from code

Inspect the README, manifests, entry points, public interfaces, migrations,
tests, assertions, and known TODOs. Derive observed behavior rather than an
aspirational rewrite:

- `§G` from the current product outcome.
- `§C` from actual stack and operational constraints.
- `§I` from public APIs, CLIs, configuration, persistence, and integrations.
- `§V` from observable behavior, tests, guards, and domain rules.
- `§T` only for concrete unfinished work or missing proof.
- `§B` empty unless confirmed history is already available.

Mark inference with `?`; do not present guesses as system truth.

## Amend

Read the named section and the references that constrain it. Preserve unrelated
sections, wording, IDs, and task status. Allocate IDs monotonically; never reuse
deleted IDs. Change direct dependencies only when needed to avoid a dangling or
contradictory reference, and call those changes out in the diff.

## Apply Backprop

Require all of the following before writing:

- traced root cause;
- evidence location;
- user-confirmed change set;
- mandatory proposed `§B` row;
- optional `§V`, `§I`, and `§T` changes;
- named regression test target when a new invariant is proposed.

Allocate final IDs, append the `§B` row, add only confirmed semantic changes,
and return the allocated IDs to Backprop. Do not edit code or commit.

## Boundaries

- Semantic `SPEC.md` writes only; no implementation, tests, verification, or git
  commit.
- No sub-agents, dashboards, auxiliary state, or speculative scaffolding.
- Preserve exact paths, identifiers, commands, and code tokens.
- A clean result is a focused diff, `SPEC_MISSING`, or `FORMAT_MISSING`; never
  silently no-op.

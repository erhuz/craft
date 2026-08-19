---
name: distill
description: >
  Compact and refine an existing repository-root SPEC.md to current intended
  truth and open work. Use only when explicitly invoked as $craft:distill to
  remove proven obsolete, duplicate, reverted, completed, or resolved ledger
  history through a preview-and-confirm rewrite. $craft:destill is the explicit
  compatibility alias. Surviving identifiers never change, and this skill never
  implements, tests, commits, or treats current code as product truth without
  operator input.
---

# Distill

Compact an existing ledger without erasing current intent. Treat the first
invocation as analysis and the confirmed second turn as the only write gate.

## Parse scope

1. Accept only the exact command `$craft:distill` with no arguments.
2. Let the companion `destill` alias registration translate exact
   `$craft:destill` to this command before applying this contract.
3. Return `INVALID_SCOPE` for punctuation, mixed commands, flags, or any other
   argument, and stop before repository inspection or writes.

## Load the ledger

1. Resolve the current Git root. If none exists, use the current directory.
2. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING`, suggest
   `$craft:spec from-code`, and stop before code inspection or writes.
3. Load exactly one format contract: read all of `<root>/FORMAT.md` when it
   exists; otherwise read all of `../caveman/SKILL.md`.
4. If the selected contract is missing or unreadable, return `FORMAT_MISSING`
   and stop.
5. Read relevant local instructions. Capture the exact `SPEC.md` bytes, Git
   `HEAD` when present, and staged, unstaged, and untracked state as the preview
   baseline.
6. If any task is `~`, name that in-flight task and stop before implementation
   inspection or writes. Distillation must not interrupt an in-flight task.

## Keep identifiers stable

Surviving `V`, `T`, and `B` rows keep the identifiers they already carry.
Removed identifiers leave permanent gaps and are never reallocated. No phase
renumbers a ledger.

Existing citations therefore stay valid across distillation, and source, tests,
documentation, and commit history may reference ledger identifiers without
becoming stale. Only a reference to a row this distillation removes goes out of
date, and the preview's Remove list already names every such identifier.

## Establish current truth

Read the complete ledger, then inspect only evidence needed to judge its current
meaning: README and product documentation, manifests, public entry points and
callers, state ownership, persistence and migrations, tests and assertions, and
current TODOs.

- Treat current operator decisions, the ledger's intended behavior, and open
  work as product intent.
- Treat committed implementation as evidence, not automatic authority.
- Label staged, unstaged, and untracked evidence; never silently adopt it as
  accepted behavior.
- Use Git history only when current artifacts cannot distinguish two material
  interpretations. Do not reconstruct history merely to preserve it.
- Mark an evidence gap as unknown. Absence of proof is never proof that a rule
  is obsolete.

## Classify every item

Build one dependency-complete replacement across `§G`, `§C`, `§I`, `§V`, `§T`,
and `§B`.

Keep:

- the current outcome, constraints, explicit non-goals, public interfaces, and
  observable behavioral rules;
- every `.` task and its cited contracts;
- unresolved defects and any item whose status remains unknown;
- current trust-boundary, authorization, data-loss, security, failure, and
  recovery rules unless direct evidence plus the operator confirms replacement.

Rewrite:

- overlapping or superseding statements into one current statement without
  losing conditions, ownership, failure behavior, or exact technical tokens;
- completed-task knowledge into the surviving interface or invariant when that
  knowledge is required to describe current behavior;
- verbose surviving text with the selected Caveman format.

Remove only with direct evidence:

- duplicate, deleted, reverted, or superseded goals, constraints, interfaces,
  and invariants that no current intent or open task requires;
- completed tasks after their outcome is proven and any lasting behavior is
  captured elsewhere;
- resolved bug rows after the fix is proven and any reusable recurrence rule
  remains encoded.

When implementation contradicts intended behavior, show the evidence and ask
the operator to choose `defect`, `changed intent`, or `unknown` for that conflict.
`defect` and `unknown` keep the intended ledger rule. A confirmed defect gets a
recommendation for explicit `$craft:backprop`; Distill never creates bug history
or normalizes the ledger to the defect. `changed intent` may support a rewrite
or removal only in the confirmed preview.

When two ledger claims express mutually exclusive intent, show both and ask
which claim remains current or whether the result is `unknown`. An explicit
`unknown` preserves both claims. Every implementation or ledger-conflict
question requires an explicit answer; conservative Keep behavior describes what
survives without an answer, not permission to confirm. Each answer changes the
semantic input and requires a new preview.

## Build the preview

Preserve required section order and table headers. Keep every surviving `V`,
`T`, and `B` identifier and every task citation exactly as they stand. Merge or
rename `§I` keys only when the preview updates every reference. Preserve
surviving task statuses.

If no material reduction or clarification exists, output only:

`No distillation needed.`

Otherwise return the preview with:

1. preview baseline identity;
2. concise Keep, Rewrite, and Remove lists with evidence;
3. all operator questions, their conservative Keep outcome, and their
   confirmation-blocking status until answered;
4. every removed `V`, `T`, and `B` identifier, plus any changed `§I` key mapping;
5. complete candidate ledger text.

Ask for explicit confirmation of that exact change set only after every semantic
question has an explicit answer. Write nothing on the preview turn. Any answer
or correction creates a new preview and invalidates the old one.

## Apply the confirmed preview

Before writing, re-resolve the root and re-read the ledger, selected format,
Git `HEAD`, worktree state, and every evidence path used by the preview. If any
material input differs, report the preview as stale, write nothing, and
regenerate it.

If any semantic question remains unanswered, name each unanswered choice and
write nothing. A general confirmation never substitutes for a missing choice.

Replace `SPEC.md` atomically with the confirmed content in one write, making no
new semantic decision during application. Create no staging, candidate,
migration, or archive file; `SPEC.md` is the only ledger any phase reads. Then
report the applied rewrite with the final diff and compact kept, rewritten, and
removed counts.

## Boundaries

- Semantic `SPEC.md` rewrite only; no code, test, format, generated file, Git
  staging, commit, push, deployment, provider, or installed-plugin mutation.
- No automatic Spec, Check, Backprop, Build, or Full Loop invocation.
- No sub-agents, auxiliary archive, dashboard, history file, or hidden state.
- Never delete uncertainty to reduce characters. Retain it until evidence or an
  operator decision resolves it.

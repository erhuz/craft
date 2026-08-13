---
name: distill
description: >
  Compact and refine an existing repository-root SPEC.md to current intended
  truth and open work. Use only when explicitly invoked as $craft:distill to
  remove proven obsolete, duplicate, reverted, completed, or resolved ledger
  history through a preview-and-confirm rewrite. $craft:destill is the explicit
  compatibility alias. This skill writes temporary candidate artifacts and never
  implements, tests, commits, or treats current code as product truth without
  operator input.
---

# Distill

Compact an existing ledger without erasing current intent. Treat the first
invocation as analysis and the confirmed second turn as the only write gate.

## Parse scope

1. Accept one of:
   - `$craft:distill`
   - `$craft:distill --candidate`
   - `$craft:distill --promote`
2. Bare `$craft:distill` and `$craft:distill --candidate` are Candidate mode.
3. Let the companion `destill` alias registration translate exact
   `$craft:destill` to this command before applying this contract.
4. Return `INVALID_SCOPE` for punctuation, mixed commands, unknown arguments,
   or malformed flag combinations and stop before repository inspection or writes.

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
6. If any task is `~`, return `ACTIVE_TASK` and stop before implementation
   inspection or writes. Distillation must not invalidate an in-flight selector
   or handoff.

## Candidate mode

1. Read repository-root `SPEC.md` as source.
2. Treat semantic implementation references to live identifiers as migration input
   only, not a hard stop.
3. On confirmation, write complete distilled content to `NEW_SPEC.md`.
4. Produce `DISTILL_MIGRATION.md` containing:
   - source `HEAD` and SPEC hash;
   - complete old-to-new/removed/merged `V/T/B` mapping;
   - changed interface-key mapping;
   - every external semantic reference location;
   - referenced old ledger text;
   - corresponding candidate ledger text;
   - required domain-language replacement.
5. On confirmation, write only `NEW_SPEC.md` and `DISTILL_MIGRATION.md`.
6. Leave `SPEC.md` unchanged and authoritative.
7. Never edit source, tests, documentation, configuration, or Git state.
8. Treat `NEW_SPEC.md` and `DISTILL_MIGRATION.md` as temporary artifacts
   exempt from identifier-usage and coupling gates.

## Reject implementation coupling

Search non-generated repository source, tests, comments, docstrings,
documentation, configuration, and runtime strings—including relevant untracked
files—for semantic references to actual live SPEC identifiers. Exact Craft
command selectors are allowed. A coincidental token matching `V<n>` or `T<n>` is
not evidence without reference context.

In Candidate mode, collect all references and include exact locations in
`DISTILL_MIGRATION.md`. Do not hard-stop on unresolved references.

In Promotion mode, if an implementation artifact explains, labels, branches on,
or otherwise depends on a live ledger identifier outside `SPEC.md`,
`NEW_SPEC.md`, and `DISTILL_MIGRATION.md`, return `SPEC_ID_REFERENCE` with
exact locations and stop. Distill owns no code fix; recommend a Spec task and
explicit Build invocation to replace each reference with domain meaning.

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

Preserve required section order and table headers. Renumber surviving `V`, `T`,
and `B` rows independently from 1 in their current relative order. Rewrite every
task citation and bug fix reference to the new IDs. Merge or rename `§I` keys
only when the preview updates every reference. Preserve surviving task statuses.

If no material reduction or clarification exists, output only:

`No distillation needed.`

Otherwise return `DISTILL_PREVIEW` with:

1. preview baseline identity;
2. concise Keep, Rewrite, and Remove lists with evidence;
3. all operator questions, their conservative Keep outcome, and their
   confirmation-blocking status until answered;
4. complete old-to-new `V`, `T`, `B`, and changed `§I` mapping;
5. complete candidate ledger text and migration summary sections.

Ask for explicit confirmation of that exact change set only after every semantic
question has an explicit answer. Write nothing on the preview turn. Any answer
or correction creates a new preview and invalidates the old one.

## Apply the confirmed preview

Before writing, re-resolve the root and re-read the ledger, selected format,
Git `HEAD`, worktree state, and every evidence path used by the preview. If any
material input differs, return `DISTILL_STALE`, write nothing, and regenerate
the preview.

If any semantic question remains unanswered, return `DISTILL_UNRESOLVED` and
write nothing. A general confirmation never substitutes for the missing choice.

In Candidate mode, replace only `NEW_SPEC.md` and `DISTILL_MIGRATION.md`
atomically with confirmed content; make no new semantic decision during
application. Then return `DISTILL_APPLIED` with the final diff and compact
kept/rewritten/removed counts.

## Promotion mode

1. Require `SPEC.md`, `NEW_SPEC.md`, and `DISTILL_MIGRATION.md` to exist.
2. Reject promotion with `DISTILL_STALE` if source `HEAD` or source SPEC hash
   changed.
3. Reject promotion with `SPEC_ID_REFERENCE` if unresolved live semantic
   references remain outside the three migration files.
4. Validate candidate sections, identifiers, citations, statuses, and interface
   mappings against current `SPEC.md`.
5. On confirmation:
   - atomically replace `SPEC.md` with `NEW_SPEC.md`;
   - remove `NEW_SPEC.md`;
   - remove `DISTILL_MIGRATION.md` or rewrite it as an identifier-free
     domain summary;
   - do not edit implementation or Git state.

Return `DISTILL_PROMOTED` on success.

## Boundaries

- Semantic `SPEC.md` rewrite only; no code, test, format, generated file, Git
  staging, commit, push, deployment, provider, or installed-plugin mutation.
- No automatic Spec, Check, Backprop, Build, or Full Loop invocation.
- No sub-agents, auxiliary archive, dashboard, history file, or hidden state.
- Never delete uncertainty to reduce characters. Retain it until evidence or an
  operator decision resolves it.

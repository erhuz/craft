---
name: check
description: >
  Reconcile the repository-root SPEC.md with current code read-only. Use when
  explicitly invoked as $craft:check or delegated by $craft:full-loop to check
  current §G, §C, §I, §V, and §T truth, narrow the scan to one of those
  sections, or verify one or more task IDs and their cited contracts. Report
  evidence and remedy hints; never write or invoke another Craft phase.
---

# Check

Compare the ledger with implementation reality. Report mismatches; let the user
decide whether code or specification must change.

## Load

1. Parse the invocation before repository inspection:
   - no argument or `--all`: check `§G`, `§C`, `§I`, `§V`, and `§T`;
   - `§G`, `§C`, `§I`, `§V`, or `§T`: check only that section;
   - one or more `T<n>` arguments: check those tasks plus their directly cited
     `§V` invariants and `§I` interfaces, in ledger order;
   - `§B`: return `INVALID_SCOPE`; append-only defect history is not current
     truth and never participates in drift;
   - mixed section, `--all`, and task-ID scopes, or any unknown scope: return
     `INVALID_SCOPE` with the accepted forms and stop.
2. Resolve the current Git root. If none exists, use the current directory.
3. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING` and stop: no
   code inspection, command execution, or write.
4. Load exactly one format contract: read all of `<root>/FORMAT.md` when it
   exists; otherwise read all of `../caveman/SKILL.md`.
5. If the selected format contract is missing or unreadable, return
   `FORMAT_MISSING` and stop.
6. Read relevant local instructions, then inspect git status and relevant diffs
   to distinguish worktree changes from committed state.

## Establish evidence

Translate each selected ledger item into an observable claim. Inspect only the
relevant public entry points, callers, state owners, configuration, migrations,
tests, and assertions. Do not infer behavior from names or comments alone.

For every reported finding, cite the `SPEC.md` item and exact `path:line`
evidence. For absence or missing proof, name the searched paths, identifiers, or
commands that establish the boundary.

Label each finding:

- `worktree`: discrepancy comes from a staged, unstaged, untracked, or dirty
  `SPEC.md` change;
- `committed`: discrepancy exists in tracked committed state;
- `unknown`: no Git repository exists or evidence cannot establish provenance.

Never treat an uncommitted implementation mistake as accepted product behavior.
Never select or classify `§B`; its rows remain append-only history.

## Check `§G`

Classify the current goal:

- `MATCH`: implementation and declared open work remain aligned with the stated
  outcome;
- `DRIFT`: direct current evidence contradicts the outcome or shows the product
  now targets a materially different outcome;
- `UNVERIFIABLE`: available source cannot prove or disprove the goal.

An unfinished legitimate open task alone is not goal drift.

## Check `§C`

Classify every current constraint and explicit non-goal:

- `MATCH`: direct source, configuration, or repository state supports it;
- `DRIFT`: direct current evidence contradicts it or resolves a condition still
  presented as current or unknown;
- `UNVERIFIABLE`: available source cannot prove or disprove it.

## Check `§I`

Classify every selected interface:

- `MATCH`: implemented public shape and ownership match the ledger;
- `DRIFT`: implementation exists but shape, ownership, or side effect differs;
- `MISSING`: required interface is absent;
- `EXTRA`: an externally reachable in-scope surface exists but is absent from
  `§I`.

Do not report internal helpers as `EXTRA`.

## Check `§V`

Classify every selected invariant:

- `HOLD`: direct code or test evidence implements the rule;
- `VIOLATE`: direct evidence contradicts the rule;
- `UNVERIFIABLE`: available source cannot prove or disprove the rule.

## Check `§T`

Classify task claims against implementation evidence:

- `VERIFIED`: an `x` task has concrete implementation or proof;
- `READY`: a selected `~` task has an unchanged Full Loop `BUILD_READY` handoff,
  concrete implementation proof, passing required gates, and holding cited
  contracts;
- `INCOMPLETE`: a specifically selected open task has direct evidence that its
  required outcome is absent or partial;
- `STALE`: status contradicts direct evidence, including an `x` task whose
  required work is absent or an open task whose full outcome is already proven
  outside a valid Full Loop handoff;
- `UNVERIFIABLE`: task wording cannot be mapped to sufficient evidence.

An open `.` or `~` status alone is not drift. In a whole-section scan, expected
unfinished work is neither `INCOMPLETE` nor a finding. A `READY` classification
requires the supplied handoff; an ordinary `~` task is never presumed ready.

## Report

Group findings under `§G`, `§C`, `§I`, `§V`, and `§T`. Omit `HOLD`, `MATCH`,
`VERIFIED`, `READY`, and expected-open task lines but count them in the summary.
Report evidence gaps separately from drift.

```text
§G
DRIFT [committed] `README.md:8` describes a different product outcome.

§C
DRIFT [worktree] `SPEC.md:6` still presents a condition resolved by `gate.py:47`.

§V
V2 VIOLATE [committed] `auth/mw.go:47` uses `<`, but V2 requires `≤`.
V5 UNVERIFIABLE [unknown] searched `auth/**`; no proof covers every request path.

§I
I.api DRIFT [worktree] `route.go:112` returns `{result}`, not `{id}`.

§T
T3 STALE [committed] `SPEC.md:31` is `x`; required middleware is absent from `auth/**`.

summary: 4 drift; 1 stale; 1 unverifiable; 8 hold/match/verified/ready.
next: <one read-only remedy hint per reported class>
```

If any selected item is `DRIFT`, `VIOLATE`, `MISSING`, `EXTRA`, `STALE`,
`INCOMPLETE`, or `UNVERIFIABLE`, do not output the clean sentinel. If every
selected item holds, matches, verifies, is ready, or is legitimately expected
open work, output only:

`No drift found.`

## Remedy hints

Suggest actions; never invoke them:

- worktree mismatch inside an active task, with correct existing `§V`/`§I`:
  resume `$craft:build <Tn>` without adding bug history;
- incomplete selected task: resume `$craft:build <Tn>`;
- committed or previously accepted defect, including false completion: invoke
  `$craft:backprop`;
- stale or intentionally changed `§G`/`§C` truth: invoke `$craft:spec amend §G`
  or `$craft:spec amend §C`;
- missing work with an open task: invoke `$craft:build <Tn>`;
- planned missing work not yet claimed complete and without a task: invoke
  `$craft:spec amend §T`;
- intentional undocumented interface: invoke `$craft:spec amend §I`;
- missing required proof: invoke `$craft:spec amend §T` to add the smallest
  verification task.

Do not recommend changing a completed task status directly through Spec; route
a committed false completion through Backprop.

## Boundaries

- Zero writes: no `SPEC.md` or code edits, tests, builds, checks, linting,
  formatting, staging, commits, pushes, deployments, or provider actions.
- No automatic Spec, Build, Backprop, or Audit invocation.
- No sub-agents, dashboards, scores, severity labels, fixes, or redesigns.
- No sibling-repository or runtime widening without explicit scope.
- Clean result is `No drift found.`, `SPEC_MISSING`, `FORMAT_MISSING`, or
  `INVALID_SCOPE`; never silently no-op.

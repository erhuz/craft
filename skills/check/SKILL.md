---
name: check
description: >
  Compare repository-root SPEC.md with current code and report drift, evidence
  gaps, and remedy hints. Use when explicitly invoked as $craft:check for the
  current ledger, one supported section, or selected task IDs. Read-only.
---

# Check

Establish whether the selected ledger claims match implementation reality.
Report mismatches with evidence and remedy hints; the user decides whether
code or specification must change. Check never writes or invokes another
Craft phase.

## Load

1. Parse the invocation before repository inspection:
   - no argument or `--all`: check `§G`, `§C`, `§I`, `§V`, and `§T`;
   - `§G`, `§C`, `§I`, `§V`, or `§T`: check only that section;
   - one or more `T<n>` arguments: check those tasks plus their directly cited
     `§V` invariants and `§I` interfaces, in ledger order;
   - `§B`: return `INVALID_SCOPE`; historical defect rows are not current truth
     and never participate in drift;
   - mixed section, `--all`, and task-ID scopes, or any unknown scope: return
     `INVALID_SCOPE` with the accepted forms and stop.
2. Resolve the current Git root. If none exists, use the current directory.
3. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING` and stop: no
   code inspection, command execution, or write.
4. Load exactly one format contract: read all of `<root>/FORMAT.md` when it
   exists; otherwise read all of `../caveman/SKILL.md`.
5. If the selected format contract is missing or unreadable, return
   `FORMAT_MISSING` and stop.
6. Use relevant local instructions, git status, and relevant diffs to
   distinguish worktree changes from committed state.

## Establish evidence

Translate each selected ledger item into an observable claim, then let that
claim determine which public entry points, callers, state owners,
configuration, migrations, tests, and assertions need inspection. Names and
comments alone do not establish behavior.

Gather enough evidence to classify each selected item without widening beyond
its claim. For every reported finding, cite the `SPEC.md` item and exact
`path:line` evidence. For absence or missing proof, name the searched paths,
identifiers, or commands that establish the boundary.

Label each finding:

- `worktree`: discrepancy comes from a staged, unstaged, untracked, or dirty
  `SPEC.md` change;
- `committed`: discrepancy exists in tracked committed state;
- `unknown`: no Git repository exists or evidence cannot establish provenance.

Never treat an uncommitted implementation mistake as accepted product behavior.
Never select or classify `§B`; its rows remain historical and are pruned only
by confirmed Distill.

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
- `INCOMPLETE`: a specifically selected open task has direct evidence that its
  required outcome is absent or partial;
- `STALE`: status contradicts direct evidence, including an `x` task whose
  required work is absent or an open task whose full outcome is already proven;
- `UNVERIFIABLE`: task wording cannot be mapped to sufficient evidence.

An open `.` or `~` status alone is not drift. In a whole-section scan, expected
unfinished work is neither `INCOMPLETE` nor a finding.

## Report

Finish when every selected item has a supported classification or an explicit
evidence gap. Group findings under `§G`, `§C`, `§I`, `§V`, and `§T`. Omit
`HOLD`, `MATCH`, `VERIFIED`, and expected-open task lines but count them in the
summary. Report evidence gaps separately from drift.

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

summary: 4 drift; 1 stale; 1 unverifiable; 8 hold/match/verified.
next: <one read-only remedy hint per reported class>
```

If any selected item is `DRIFT`, `VIOLATE`, `MISSING`, `EXTRA`, `STALE`,
`INCOMPLETE`, or `UNVERIFIABLE`, do not output the clean sentinel. If every
selected item holds, matches, verifies, or is legitimately expected
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
- No automatic Spec, Distill, Build, Backprop, or Audit invocation.
- No sub-agents, dashboards, scores, severity labels, fixes, or redesigns.
- No sibling-repository or runtime widening without explicit scope.
- Clean result is `No drift found.`, `SPEC_MISSING`, `FORMAT_MISSING`, or
  `INVALID_SCOPE`; never silently no-op.

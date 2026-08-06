---
name: build
description: >
  Plan and implement tasks from the repository-root SPEC.md in one native,
  single-thread loop. Use only when explicitly invoked as $craft:build, usually
  with --next, --all, or a task ID. Own code, tests, verification, task status,
  exact staging, and the task commit. Route semantic spec failures through
  $craft:backprop and $craft:spec.
---

# Build

Implement one approved SPEC task at a time. Own code and verification; do not
own semantic spec content.

## Load

1. Resolve the current Git root. If none exists, use the current directory.
2. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING` and stop: no
   edits, tests, speculation, or commit.
3. Read local instructions, `FORMAT.md` when present, and the contracts in
   `../ponytail/SKILL.md` and `../caveman/SKILL.md`.
4. Inspect git status before selecting work. Preserve unrelated user changes.

## Select

- `<task-id>`: select that task only.
- `--next` or no argument: select the lowest-numbered open task (`.` first,
  then an already-started `~` task that belongs to this worktree).
- `--all`: process open tasks in order, committing each verified task before
  starting the next.
- No open task: strict no-op; report it and stop.

Do not begin a new task while known current-task changes remain unstaged or
uncommitted. Reconcile that slice first.

## Plan

Trace the task through current callers and state ownership. Produce the smallest
executable plan that names:

- selected task and applicable `§V` invariants;
- touched `§I` interfaces;
- exact files expected to change;
- one smallest regression or behavior check per non-trivial rule;
- focused and final verification commands.

The explicit Build invocation authorizes this scoped plan. Pause only for a new
product decision, external side effect, missing permission, or meaningful scope
expansion.

## Execute

For each selected task:

1. Change only its status cell from `.` to `~`.
2. Implement the root behavior at the shared ownership point using Ponytail's
   smallest-correct ladder.
3. Add the smallest runnable check that would fail for the defect or behavior.
4. Run the focused check, then the repository's required test, check, lint, or
   build gates in the task's scope.
5. On success, change only the status cell from `~` to `x`.
6. Review the final diff, stage exactly the task files plus `SPEC.md`, run staged
   whitespace/name checks, and commit immediately.

Feature commit: `T<n>: <goal>` with relevant `V<n>` references in the body when
useful. A Backprop fix commits spec, test, and code together as
`backprop B<n> + V<n>: <cause>`; omit `+ V<n>` when no invariant was added.

## Failure routing

Classify before retrying:

- Existing `§V`/`§I` already requires the right behavior and the current
  uncommitted implementation violates it: fix the code inside Build and retry.
  Do not create bug history for an implementation typo caught before completion.
- The specification is missing, wrong, or allowed the failed behavior: keep the
  task `~`, invoke `$craft:backprop`, wait for its semantic proposal to be
  confirmed and applied through `$craft:spec`, then resume this task.
- Failure is unrelated, environmental, permission-bound, or external: report the
  exact blocker and leave the task `~`. Do not turn a transient condition into a
  spec rule unless it is a durable product or operational constraint.

Never retry blindly. A non-zero command is evidence to classify, not automatic
proof that the specification is wrong.

## Completion gate

Mark and commit a task complete only when:

- focused verification passes;
- required repository-wide gates for this task pass;
- applicable invariants remain true;
- only intended files are staged;
- unrelated worktree changes remain untouched.

## Boundaries

- Only task status cells may be changed directly in `SPEC.md`; all semantic
  changes go through `$craft:spec`.
- No sub-agents, parallel workers, progress dashboards, or speculative work.
- Never widen into sibling repositories, services, deployments, or provider
  state without explicit scope.

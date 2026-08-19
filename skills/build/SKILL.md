---
name: build
description: >
  Plan and implement explicitly requested tasks from one or more SPEC.md
  ledgers in one native single-thread loop. Use when explicitly invoked as
  $craft:build with any task, selector, path, ledger set, or natural-language
  scope, or when delegated by $craft:full-loop. Own code, tests, verification,
  task status, exact staging, and each task commit. Route semantic spec failures
  through $craft:backprop and $craft:spec.
---

# Build

Implement one approved SPEC task at a time. Own code and verification; do not
own semantic spec content.

## Interpret request

1. Treat exact first token `$craft:build` as implementation authorization. Do
   not apply an argument whitelist or reject multiple IDs, selectors, paths,
   ledgers, or unfamiliar flags solely because of command shape.
2. Treat the remaining prompt as the requested scope. Accept any explicit
   combination that can be resolved to concrete ledgers and tasks; one
   invocation may span multiple ledgers.
3. Treat no remaining scope as `--next` in the current repository-root ledger.
4. Resolve unclear wording through read-only inspection. If the requested
   ledger/task mapping still has more than one materially different meaning,
   state that exact ambiguity and ask one focused question before mutation.

## Load

1. Resolve every ledger named or described by the request:
   - no explicit ledger target → current Git root, or current directory when
     no Git root exists;
   - explicit `SPEC.md`, file, or directory targets → those exact project
     ledgers;
   - a named child, descendant, or repository set → discover ledgers only
     within that stated boundary.
2. Normalize real paths, deduplicate ledgers, and sort them lexically. Resolve
   each ledger's containing Git root separately for baselines and commits.
3. Read every resolved `SPEC.md`. A requested target without one returns
   `SPEC_MISSING` and stops the whole preflight before mutation.
4. For every explicit task ID, inspect its ledger row:
   - absent ID → return `TASK_NOT_FOUND` and stop;
   - `x` → report `TASK_ALREADY_COMPLETE` as a per-task strict no-op and
     continue preflighting other requested tasks.
5. Read local instructions and `FORMAT.md` for every selected ledger when
   present, plus the contracts in `../ponytail/SKILL.md` and
   `../caveman/SKILL.md`.
6. Inspect Git status for every selected ledger before selecting work. Preserve
   unrelated user changes.

## Select

- Explicit task IDs: accept one or more, preflight all of them, and process each
  ledger's selected tasks in ledger order. Select both `.` and `~`; resume `~`
  from the current worktree state without requiring ownership proof.
- `--next`, in order:
  1. If any `~` tasks exist, resume the lowest-numbered one before any `.` task.
  2. Otherwise, select the lowest-numbered `.` task.
  3. If no `.` or `~` task exists, strict no-op. Report it and stop.
- `--all`: process every `~` and `.` task in ledger order, committing each
  verified task before starting the next.
- Multiple ledgers or selector clauses: apply each requested selector to its
  resolved target. Preflight the full ledger/task mapping before mutation, then
  process ledgers lexically and tasks in ledger order.

`TASK_NOT_FOUND` exits before code inspection, tests, Git-status handling, or
mutation.

Treat every selected `~` task and existing worktree change as resumable input.
Never require attribution to an earlier session before continuing.

## Plan

Trace the task through current callers and state ownership. Produce the smallest
executable plan that names:

- exact Build command selector, selected goal, and applicable invariant text;
- touched interface contracts by domain meaning;
- exact files expected to change;
- one smallest regression or behavior check per non-trivial rule;
- focused and final verification commands.

The explicit Build invocation, or a task delegated by an explicit Full Loop
invocation, authorizes this scoped plan. Pause only for a new product decision,
external side effect, missing permission, or meaningful scope expansion.

## Implementation artifact contract

Use domain meaning rather than volatile ledger labels throughout implementation:

- Actual SPEC identifiers may appear only inside `SPEC.md` and exact Craft
  command selectors. Never copy them into source, comments, docstrings, tests,
  test names, snapshots, fixtures, documentation, configuration, runtime output,
  commit messages, or handoff prose.
- Identify the selected task in working output only through its exact Build
  command selector. Describe its goal, invariants, and interfaces by content,
  without standalone ledger labels.
- During active Distill migration, allow temporary candidate identifiers in
  `NEW_SPEC.md` and `DISTILL_MIGRATION.md` to support external-reference
  replacement planning. Build may read migration mappings to replace references
  with stable domain language, but `SPEC.md` remains authoritative until
  explicit `$craft:distill --promote`.
- Write every code comment and docstring only in English, regardless of the
  implementation language. Give every authored or materially changed
  non-generated function, including test functions, a comment or docstring
  using that language's normal syntax that explains its intended use and why it
  exists. Generated and vendored functions are exempt; Build still introduces
  no SPEC identifiers into them.
- Review the task diff for this contract before running final gates.

## Git baseline

After planning expected paths and before any mutation:

1. Record baseline `HEAD` and exact index/worktree state.
2. Continue from current staged, unstaged, and untracked content without
   requiring task-ownership proof.
3. Apply the smallest task change atop that state without resetting, stashing,
   overwriting, or discarding pre-existing content.
4. Stage Build-introduced changes separately when safe. If existing content in
   a selected task path cannot be separated, preserve and include the path as it
   stands instead of blocking. Keep unrelated paths' baseline worktree bytes and
   index entries unchanged.

## Execute

For each selected task:

1. Change only its status cell from `.` to `~`.
2. Implement the root behavior at the shared ownership point using Ponytail's
   smallest-correct ladder.
3. Add the smallest runnable check that would fail for the defect or behavior.
4. Run the focused check, then the repository's required test, check, lint, or
   build gates in the task's scope.
5. On success, change only the status cell from `~` to `x`.
6. Review the final diff, stage the selected task files plus `SPEC.md` while
   preserving their baseline content, run staged whitespace/name checks for
   those paths, and commit exactly those paths immediately. If unrelated paths
   were already staged, use a path-limited commit and verify their index entries
   remain unchanged. Verify all unrelated baseline worktree bytes and index
   entries remain unchanged after commit.

When one invocation selects multiple tasks or ledgers, finish this entire flow
and its task commit before moving to the next. Stop on the first blocker or
failed verification, report completed, blocked, and untouched work, and do not
roll back commits already completed by this invocation.

Feature commit: `build: <goal>`. A Backprop fix commits spec, test, and code
together as `fix: <root cause>`. Keep the subject and body free of ledger
identifiers.

## Full Loop handoff

Direct Build invocations keep the Execute flow above. When delegated by Full
Loop, split ownership into review and finalization:

1. In review mode, perform Execute steps 1–4, leave the task `~`, and do not
   stage or commit.
2. Return `BUILD_READY` with the exact delegated Build command selector,
   selected goal and applicable contract text without ledger labels, baseline
   `HEAD`, exact task-owned paths and diff, and focused plus final gate commands
   and results.
3. If Full Loop returns review findings, classify them through Failure routing,
   repair only the authorized task slice, rerun its gates, and return a fresh
   `BUILD_READY`. Any code, test, interface, or semantic spec edit invalidates
   prior Audit and Check results.
4. Finalize only when Full Loop supplies exact clean results from both reviewers
   for the unchanged handoff. Verify baseline `HEAD`, task-owned diff, and
   unrelated dirty paths; then perform Execute steps 5–6 and return the commit
   SHA. The `~` → `x` status edit is the only expected post-review content
   change before staging.

Never accept one reviewer, summarized success, or stale review evidence as the
finalization gate. A clean handoff without its commit remains incomplete.

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
- the task commit contains only intended files;
- unrelated baseline worktree bytes and index entries remain unchanged.

When delegated by Full Loop, also require unchanged `BUILD_READY` evidence and
exact clean Audit and Check results supplied by that coordinator.

## Boundaries

- Only task status cells may be changed directly in `SPEC.md`; all semantic
  changes go through `$craft:spec`.
- No sub-agents, parallel workers, progress dashboards, or speculative work.
- The explicit Build request defines ledger and task scope. Never widen beyond
  its resolved targets into other repositories, services, deployments, or
  provider state.

---
name: build
description: >
  Plan and implement tasks from the repository-root SPEC.md in one native,
  single-thread loop. Use when explicitly invoked as $craft:build, usually with
  --next, --all, or a task ID, or when delegated by $craft:full-loop. Own code,
  tests, verification, task status, exact staging, and the task commit. Route
  semantic spec failures through $craft:backprop and $craft:spec.
---

# Build

Implement one approved SPEC task at a time. Own code and verification; do not
own semantic spec content.

## Parse scope

1. Parse the invocation before repository inspection. Accept only:
   - `$craft:build` or `$craft:build --next`;
   - `$craft:build --all`;
   - `$craft:build T<n>` with exactly one task ID.
2. Treat no selector as `--next`.
3. Reject mixed selectors, multiple task IDs, duplicate flags, and unknown
   arguments as `INVALID_SCOPE`, then stop without repository inspection or
   writes.

## Load

1. Resolve the current Git root. If none exists, use the current directory.
2. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING` and stop: no
   edits, tests, speculation, or commit.
3. For an explicit `T<n>`, inspect only its ledger row:
   - absent ID → return `TASK_NOT_FOUND` and stop;
   - `x` → return `TASK_ALREADY_COMPLETE` as a strict no-op and stop.
4. Read local instructions, `FORMAT.md` when present, and the contracts in
   `../ponytail/SKILL.md` and `../caveman/SKILL.md`.
5. Inspect git status before selecting work. Preserve unrelated user changes.

## Select

- Explicit `T<n>`:
  1. Select `.` only when no known current task blocks new work.
  2. Resume `~` only when this worktree provably owns it; otherwise return
     `TASK_OWNERSHIP_AMBIGUOUS` and stop before planning or mutation.
- `--next`, in order:
  1. If exactly one `~` task is provably owned by this worktree, resume it
     before any `.` task.
  2. If multiple `~` tasks exist or any `~` task's ownership is ambiguous,
     stop before mutation.
  3. Otherwise, select the lowest-numbered `.` task.
  4. If no `.` or `~` task exists, strict no-op. Report it and stop.
- `--all`: process open tasks in order, committing each verified task before
  starting the next.

`INVALID_SCOPE`, `TASK_NOT_FOUND`, and `TASK_ALREADY_COMPLETE` exit before code
inspection, tests, Git-status inspection, or mutation. `TASK_OWNERSHIP_AMBIGUOUS`
may follow read-only Git ownership inspection but stops before planning or
mutation.

Do not begin a new task while known current-task changes remain unstaged or
uncommitted. Reconcile that slice first.

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
- Give every authored or materially changed non-generated function, including
  test functions, a language-appropriate comment or docstring explaining its
  intended use and why it exists. Generated and vendored functions are exempt;
  Build still introduces no SPEC identifiers into them.
- Review the task diff for this contract before running final gates.

## Git ownership gate

After planning expected paths and before any mutation:

1. Record baseline `HEAD` and exact index/worktree state.
2. Treat `SPEC.md` plus every expected task file as intended task paths.
3. If any intended path has pre-existing staged, unstaged, or untracked content
   not provably owned by this task, return `TASK_PATH_OVERLAP` and stop before
   mutation. Separate hunks do not make a shared path safe.
4. Permit unrelated dirty paths only when their baseline worktree bytes and
   index entries can be verified unchanged after the task commit.

## Execute

For each selected task:

1. Change only its status cell from `.` to `~`.
2. Implement the root behavior at the shared ownership point using Ponytail's
   smallest-correct ladder.
3. Add the smallest runnable check that would fail for the defect or behavior.
4. Run the focused check, then the repository's required test, check, lint, or
   build gates in the task's scope.
5. On success, change only the status cell from `~` to `x`.
6. Review the final diff, stage only the task files plus `SPEC.md` beyond the
   baseline index, run staged whitespace/name checks for those paths, and commit
   exactly those task paths immediately. If unrelated changes were already
   staged, use a path-limited commit and verify their index entries remain
   unchanged. Verify all unrelated baseline worktree bytes and index entries
   remain unchanged after commit.

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
- Never widen into sibling repositories, services, deployments, or provider
  state without explicit scope.

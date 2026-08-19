---
name: full-loop
description: >
  Coordinate Build, Audit, and Check for repository-root SPEC.md tasks. Use
  only when explicitly invoked as $craft:full-loop for --next, --all, or one
  or more task IDs, optionally with bounded --loop repairs. Finish each task
  only after both reviewers pass and Build creates its scoped commit.
---

# Full Loop

Drive one task at a time through Build → Audit → Check. Coordinate the phases;
never write code or specification, change task status, stage, or commit directly.

## Load and validate

1. Parse the invocation before repository inspection. Accept only:
   - `$craft:full-loop` or `$craft:full-loop --next`;
   - `$craft:full-loop --all`;
   - `$craft:full-loop T<n> [T<n> ...]`;
   - any accepted selector followed by `--loop` and optional `--max N`.
2. Treat no selector as `--next`. Reject mixed selectors, duplicate flags,
   unknown arguments, non-positive `N`, and `--max` without `--loop` as
   `INVALID_SCOPE`, then stop without repository inspection or writes.
3. Resolve the current Git root. If none exists, use the current directory.
4. Read only `<root>/SPEC.md`. If absent, return `SPEC_MISSING` and stop.
5. Load exactly one format contract: all of `<root>/FORMAT.md` when present;
   otherwise all of `../caveman/SKILL.md`. If unreadable, return
   `FORMAT_MISSING` and stop.
6. Read all of `../build/SKILL.md`, `../audit/SKILL.md`, and
   `../check/SKILL.md`. If any is unreadable, name the file, report that its
   contract could not be loaded, and stop.
7. Read relevant local instructions and inspect Git status. Preserve every
   unrelated staged, unstaged, and untracked path.

The explicit Full Loop invocation authorizes the selected Build mutations,
tests, exact task commit, and read-only Audit and Check. It does not authorize
semantic specification changes, sibling repositories, deployment, provider
actions, or other external side effects.

## Select tasks

- `--next`, in order:
  1. If any `~` tasks exist, resume the lowest-numbered one before any `.` task.
  2. Otherwise, select the lowest-numbered `.` task.
  3. If no `.` or `~` task exists, strict no-op. Return `NO_OPEN_TASKS`.
- Explicit IDs: before any mutation, require every ID to exist and have `.` or
  `~` status. Process the unique tasks in ledger order, not argument order.
- `--all`: snapshot every initially open `.` and `~` task in ledger order.
  Tasks added later are outside this invocation.

Do not start a new task while a prior selected task has uncommitted changes.
Continue selected tasks from current worktree content without requiring
ownership attribution or blocking on existing content in selected paths.
Unrelated dirty paths may remain throughout.

With `--loop`, default `--max` to `1`. `N` counts returns to Build after the
initial review, not review passes, and resets for each selected task.

## Run one task

For each selected task:

1. Record baseline `HEAD`, current status, and unrelated dirty paths.
2. Delegate the task to Build in Full Loop review mode. Build implements and
   verifies it, leaves it `~`, and returns a review handoff with the exact
   delegated Build command selector, domain contract text, task-owned diff, and
   evidence. Do not review a blocked or incomplete handoff.
3. Delegate to Audit with the task goal, cited contract content without ledger
   labels, baseline, exact task-owned diff, and verification evidence.
   Explicitly request one minimal `Remedy:` per issue.
4. Regardless of Audit findings, delegate to Check as `$craft:check T<n>` with
   the same handoff evidence. Keep both phases read-only and sequential.
5. Pass only when both reviewers report nothing left to change. Judge each
   report on its content, not on matching a fixed string: a reworded clean
   result still passes, and a clean-sounding sentence carrying a caveat, an
   unresolved evidence gap, or an open finding does not.
6. Before finalization, verify `HEAD` and the reviewed task-owned diff are
   unchanged and no unrelated path became staged. Any changed implementation,
   test, interface, or semantic spec content invalidates both reviews.
7. Delegate finalization to Build with both clean results. Build alone changes
   `~` to `x`, stages the exact slice, runs staged gates, and commits. Record
   the returned commit SHA before selecting another task.

Audit and Check must both run on every review pass. Never treat partial output,
an evidence gap, `UNVERIFIABLE`, or one clean reviewer as a pass.

## Handle findings

Collapse overlapping Audit and Check findings into one evidence-backed repair
input; preserve each distinct location, violated contract, and minimal remedy.

- Without `--loop`, report the outstanding findings and stop. Leave the task
  `~`, its slice uncommitted, and unrelated changes untouched.
- With `--loop`, if the per-task return count is below `N`, increment it and
  return the combined findings to Build. Build classifies and repairs them,
  reruns focused and final gates, and produces a fresh handoff. Then rerun both
  Audit and Check.
- If findings remain after `N` returns to Build, report that the repair limit
  was reached and what remains. Leave the task `~` and uncommitted.
- Stop early, naming the exact obstacle, when evidence is insufficient for an
  actionable change, a required permission or external state is unavailable,
  or another retry would be blind.

Code-local mistakes already governed by existing `§V` or `§I` return directly
to Build without bug history. Missing, wrong, or permissive specification uses
Build's failure routing: Backprop proposes the semantic change, waits for user
confirmation, Spec applies it, and only then may this task resume. Full Loop
never confirms product semantics itself. A new separate task or meaningful
scope expansion requires a fresh explicit invocation; do not append it to this
task or an `--all` snapshot.

## Finish

Report the run complete only after every selected task has a clean result from
both reviewers and its own verified commit. Include task goals, commit SHAs, and each
task's return-to-Build count; use an exact Craft command selector only when a
task must be disambiguated. A committed task is complete; a clean but uncommitted
handoff is not.

## Boundaries

- Single thread only: no sub-agents, parallel phases, dashboards, or auxiliary
  state. `SPEC.md`, the worktree, review evidence, and Git commits are the record.
- Full Loop coordinates; Build owns all writes and commits, Audit owns material
  decision review, and Check owns spec-to-code drift review.
- Never skip, reorder, combine, or silently reinterpret a phase.

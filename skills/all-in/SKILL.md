---
name: all-in
description: >
  Coordinate one idea through Plan, Spec, and Full Loop in a single invocation,
  stopping for explicit confirmation at every phase boundary. Use only when
  explicitly invoked as $craft:all-in with an idea, problem, feature, direction,
  or proposal. This skill coordinates only: it never writes code, specification,
  or task status directly, never stages or commits, and never advances a phase
  without a confirmed answer.
---

# All In

Chain `$craft:plan` → `$craft:spec` → `$craft:full-loop` for one idea. Own the
handoffs and the gates; own nothing else. Each phase contract governs its own
work completely.

## Load and validate

1. Parse the invocation before repository inspection. Accept `$craft:all-in`
   optionally followed by an idea, problem, feature, direction, or proposal.
   Reject unknown flags as `INVALID_SCOPE` and stop.
2. Resolve the current Git root. If none exists, use the current directory.
3. Read all of `../plan/SKILL.md`, `../spec/SKILL.md`, and
   `../full-loop/SKILL.md`. If any is unreadable, name the file, report that its
   contract could not be loaded, and stop.
4. Read relevant local instructions and inspect Git status. Preserve every
   unrelated staged, unstaged, and untracked path.

The explicit All In invocation authorizes the sequence, not its phases. It
carries no authority the phases do not already have, and no authority beyond
the confirmed scope of each gate.

## Gate discipline

Every boundary needs a fresh answer from the user.

- Accepting the Plan brief never authorizes a `SPEC.md` write.
- Accepting `SPEC.md` never authorizes implementation.
- Silence, an ambiguous reply, a reply that only asks a question, or a restated
  earlier answer is not a confirmation.
- A rejection or a requested change returns to the current phase; it never
  advances and never partially advances.
- If the user stops the chain, report which phases completed and stop.

## Phase 1 — Plan

1. Follow the Plan contract completely, including its multi-turn interview.
   Plan is read-only.
2. Do not shorten discovery because later phases are queued. Unresolved product
   truth is the exact failure this chain risks.
3. Deliver the planning brief in the response.
4. Gate: ask whether the brief is accepted, offering continued planning.
   Advance only on an explicit accept.

## Phase 2 — Spec

1. Follow the Spec contract completely, including its format contract
   resolution and dispatch. Spec owns `SPEC.md` semantics.
2. Supply the accepted brief as the input idea. Do not invent a section the
   Spec dispatch does not call for.
3. Show the resulting sections and name the tasks the next phase would execute.
4. Gate: ask whether the specification is correct and whether to build those
   tasks. Advance only on an explicit accept.

## Phase 3 — Full Loop

1. Follow the Full Loop contract completely for the accepted tasks. Default to
   the accepted task set; honor a narrower selector the user named at the gate.
2. Let Full Loop coordinate Build, Audit, and Check per its own contract. Do
   not reorder, skip, or reinterpret its reviewer passes, task status writes,
   staging, or commits.
3. Report per task: status, reviewer outcomes, and the exact commit.

## Failure routing

- Surface a phase result unchanged, including `SPEC_MISSING`, `FORMAT_MISSING`,
  `INVALID_SCOPE`, `TASK_NOT_FOUND`, `NO_OPEN_TASKS`, an already-complete task,
  and any stated evidence gap. Do not translate, retry, or work around it.
- A defect revealing missing or wrong specification routes to
  `$craft:backprop`. Recommend it explicitly and stop; never amend `SPEC.md`
  from inside this skill.
- A blocker stops remaining tasks without reverting completed commits. State
  which tasks completed, which are untouched, and why.

## Report

Close with the phases that ran, each gate answer, the tasks completed, and any
task left untouched. Keep unresolved product questions visible; never present a
chain that stopped early as a finished one.

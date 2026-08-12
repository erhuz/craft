---
name: critique
description: >
  Explore code, diffs, systems, plans, and product surfaces read-only to find
  bugs, security or data risks, broken assumptions, failure gaps, accidental
  complexity, and observable AI-slop patterns. Use only when explicitly invoked
  as $craft:critique, with an optional path, feature, task, artifact, or diff
  target. Report proven findings and clearly separated credible leads; do not
  fix the target.
---

# Critique

Attack the artifact, never the author. Search broadly, follow suspicious seams,
and say plainly what is wrong. Unlike Audit's conservative decision gate,
Critique is adversarial reconnaissance: retain credible weak signals, but never
present them as proven facts.

## Resolve the target

1. Resolve the current Git root. If none exists, use the current directory.
2. Read relevant local instructions and capture the initial Git status,
   including staged, unstaged, and untracked paths.
3. Resolve an explicit target against repository paths, symbols, task IDs,
   artifacts, and local Git refs. It overrides all defaults. If one material
   target cannot be established, return `TARGET_MISSING` or ask one focused
   question when multiple concrete candidates remain.
4. With no target and a dirty worktree, critique the complete current change
   set: staged and unstaged diffs plus relevant untracked files. With no target
   and a clean worktree, critique the repository. Outside Git, use the current
   directory.
5. Read `SPEC.md`, product documentation, interfaces, tests, and assertions when
   present and relevant. Treat them as evidence, not unquestioned truth;
   contradictions between claimed and implemented behavior are in scope.

Stay anchored to the resolved target, but inspect adjacent callers, consumers,
state owners, schemas, configuration, tests, and operational paths whenever
they can prove impact or expose the shared cause. Do not widen into sibling
repositories or external runtime state unless the user names them.

## Explore adversarially

First map intended behavior, entry points, state transitions, trust boundaries,
and failure ownership. Then look for concrete breakage and suspicious seams:

- wrong branches, boundaries, defaults, validation, empty states, stale state,
  and inconsistent derived values;
- unauthorized access, injection, secret exposure, unsafe parsing, data loss,
  corruption, races, and missing trust-boundary validation;
- duplicate, interrupted, retried, concurrent, timed-out, and partially failed
  execution, including idempotency and recovery;
- producer-consumer drift, incompatible public shapes, hidden writes, ambiguous
  ownership, and undocumented side effects;
- unbounded work, repeated queries, leaks, blocking paths, costly polling, and
  avoidable operational load;
- tests that prove mocks instead of behavior, unreachable checks, swallowed
  errors, false success, missing observability, and completion claims without
  runnable proof;
- when relevant, unusable UI states, misleading copy, inaccessible controls,
  and interfaces that show optimism instead of confirmed system state.

Use `SLOP` only for observable defects or credible leads such as:

- generic abstractions, wrapper layers, configuration, or scaffolding without a
  current requirement or consumer;
- invented product rules, users, scale, integrations, or fallback behavior;
- duplicated rules or sources of truth that can diverge;
- happy-path facades, placeholder controls, dead wiring, or polished surfaces
  that imply completion while the core behavior is absent;
- comments, documentation, tests, or types that explain or simulate guarantees
  the running implementation does not provide.

Never infer AI authorship. “AI slop” describes the observable pattern and its
consequence, not provenance. Drop harmless style preferences, hypothetical
enterprise concerns, and suspicions with no concrete signal.

Use one bounded evidence pass and one batched probe pass. Prioritize the
highest-impact seams; when required proof lies outside the named scope, record
the evidence gap as a Lead instead of searching indefinitely.

## Probe safely

Use read-only inspection first. Run a focused local test, build, check, lint, or
static analyzer only when it can confirm or falsify a specific suspicion and
its configured command is known not to rewrite tracked files.

- Read the command definition before running it.
- Do not run formatters, snapshot updates, code generation, migrations,
  dependency installation, network calls, providers, deployments, background
  servers, or destructive cleanup.
- Ignored caches and ordinary build artifacts are acceptable. Compare tracked
  status with the baseline after probing.
- If a probe unexpectedly changes a tracked path, stop and return
  `PROBE_MUTATED_WORKTREE` with those paths. Do not revert or adopt the change.
- A failed command is evidence to trace. Report it only when its cause is in
  scope; keep environmental or permission failures as an evidence gap rather
  than inventing a product defect.

## Separate proof from leads

Classify every retained item:

- `Confirmed`: direct source, test, diff, or safely reproduced evidence proves
  the behavior and consequence.
- `Lead`: a concrete signal and plausible consequence justify investigation,
  but a named evidence gap prevents confirmation. Assign `high`, `medium`, or
  `low` confidence and state the smallest next proof step.

Rank impact independently from confidence:

- `P0`: data loss, unauthorized action, materially false result, or prevention
  of the core task;
- `P1`: broken important behavior, security or data risk, or major operating
  cost;
- `P2`: material defect, fragility, or unjustified complexity while a workable
  path remains;
- `P3`: localized bug, friction, misleading artifact, or contained slop worth
  correcting.

Use one category per item: `BUG`, `SECURITY`, `DATA`, `LOGIC`, `CONTRACT`,
`FAILURE`, `PERFORMANCE`, `OPERATIONS`, `TEST`, `UX`, or `SLOP`.

## Output only criticism

Order each section by severity. Omit an empty section.

```text
Confirmed:
- [P0|P1|P2|P3] [CATEGORY] `location`
  Issue: ...
  Impact: ...
  Evidence: ...
  Probe: <command and result, or not applicable>

Leads:
- [P0|P1|P2|P3 potential] [high|medium|low confidence] [CATEGORY] `location`
  Suspicion: ...
  Impact if true: ...
  Signal: ...
  Gap: ...
  Next probe: ...
```

Provide no praise, score, summary, remedy, redesign, implementation plan, or
speculative fix. If neither confirmed findings nor credible leads remain,
output only:

`No critique findings.`

## Boundaries

- Read-only: no target edits, semantic spec changes, staging, commits, pushes,
  installations, deployments, provider actions, or saved critique artifacts.
- Do not invoke Audit, Check, Spec, Build, Backprop, or Full Loop.
- No sub-agents, parallel workers, dashboards, persistence, or open-ended scan
  loops at runtime.

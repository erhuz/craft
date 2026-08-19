---
name: audit
description: >
  Audit decision-bearing artifacts such as proposals, specifications, system
  and UI designs, diffs, implementations, skills, workflows, and configuration.
  Use when explicitly invoked as $craft:audit or delegated by $craft:full-loop.
  Report only material decision-quality issues: unsupported value, invented
  product truth, unjustified complexity, broken logic, state mismatch, false
  completeness, missing failure behavior, and evidence gaps. Remain read-only;
  do not praise, summarize, redesign, fix, or advance into Spec or Distill unless
  explicitly requested.
---

# Audit

Poke holes in decisions, not authors. Never claim AI provenance without proof.
Detect the recurring failure mode—plausible-looking choices substituted for
product truth—by testing evidence and consequences, not by labeling aesthetics
as “AI slop.”

Report only supported, consequential issues. Do not duplicate a general style,
security, drift, or over-engineering review; inspect the decisions behind the
target. Stay read-only.

## Resolve scope and evidence

Honor the exact target and local instructions. Inspect adjacent artifacts only
when a material claim cannot be judged without them; do not widen into unrelated
systems.

- Proposal or spec: inspect claims, internal logic, value, scope, and stated
  evidence. Do not demand runtime proof for claims it does not make.
- Code, system design, or diff: trace relevant callers, state ownership, side
  effects, failure paths, and existing native or local alternatives.
- UI: inspect the rendered primary flow and relevant states when available.
  Unavailable proof is an evidence gap, not an invented UI defect.
- Skill, workflow, or config: inspect trigger, declared scope, decision flow,
  contracts, failure behavior, metadata, authority, and operational effects.

Before reporting, identify the material in-scope claims, available evidence, and
proof required for conclusions that cannot yet be reached. Report missing
evidence only when a material conclusion depends on it.

## Challenge the decision

Use these as search questions, never as forced labels:

- Which current user need, business premise, domain invariant, or operational
  constraint requires this?
- What breaks if the component, layer, setting, state, or step is deleted?
- Was a native or already-present capability rejected for an observed reason?
- Is this product truth, or a familiar pattern filled into an evidence gap?
- Is there one authoritative owner for each state and transition?
- Does the UI show confirmed system state, or local optimism?
- What happens for invalid, empty, unauthorized, stale, duplicate, interrupted,
  concurrent, retried, and partially failed execution?
- Is present value proportional to adoption, operation, and maintenance cost?

Collapse multiple symptoms into the shared bad decision. Omit harmless
imperfections and concerns without a concrete consequence.

## Business value

Report `VALUE` only when observed or inferred evidence shows that:

- success measures shipped output rather than behavior, revenue, cost,
  retention, or risk;
- an existing workflow delivers the outcome more cheaply;
- adoption or operating burden erases expected value;
- speculative users, scale, integrations, or configurability drive current
  scope;
- a technical capability is presented as customer value without a credible
  link.

Missing business context alone is not proof of absent value. Use `EVIDENCE` for
a material unsupported value claim.

## System and logic

Report `SYSTEM` or `LOGIC` when evidence shows that:

- a service, queue, cache, event, abstraction, repository, plugin layer, or
  setting has no current requirement or consumer;
- derived state is persisted unnecessarily or sources of truth can diverge;
- business rules are duplicated across clients, services, jobs, or storage;
- UI shape dictates the domain model rather than domain invariants;
- authorization or trust-boundary validation exists only in the client;
- reads hide writes, retries are unsafe, or partial failure corrupts state;
- fallbacks convert contract failure into empty data or apparent success;
- generic error handling hides which operation failed;
- ownership of state, transitions, or integrations is ambiguous;
- mock-heavy tests prove wiring but not observable behavior;
- scaffolding or polish implies completion while the core path is unproven;
- the procedure's trigger, promise, output, permissions, or dependencies make
  its promised result unreachable.

## UI decisions

Report `UI` when evidence shows that:

- navigation or information architecture follows available components instead
  of the user's task;
- a generic dashboard, card grid, wizard, tab set, or modal adds steps without
  improving comprehension or control;
- the primary action competes with equally prominent actions;
- context disappears and must be remembered, or labels and domain terms force
  guessing;
- success appears before persistence or external confirmation;
- loading, empty, stale, unauthorized, error, retry, or partial-success states
  contradict system truth;
- destructive or costly actions lack proportional prevention, cancellation,
  confirmation, or recovery;
- help text compensates for an unclear workflow;
- custom controls replace clearer native controls without demonstrated need;
- keyboard access, focus, semantics, contrast, zoom, touch targets, or responsive
  ordering blocks the actual task;
- decoration weakens hierarchy, specificity, comprehension, accessibility, or
  performance;
- controls are placeholders, local-only, or fabricated while appearing real.

Never report a visual trope merely because generative systems often produce it.
Require a user, system, or business consequence.

## Evidence and severity

For every issue:

- identify the exact claim, control, state, section, or source location;
- name the violated need, premise, invariant, or system truth;
- state the concrete consequence;
- label evidence `observed`, `inferred`, or `missing`;
- use `missing` only for `EVIDENCE`, never as proof of a substantive defect;
- use P0 only with observed evidence; inferred issues may be P1 or P2;
- omit praise, scores, summaries, stylistic preferences, hypothetical enterprise
  concerns, fixes, alternatives, and roadmaps unless explicitly requested.

Severity:

- `P0`: observed data loss, unauthorized action, materially false result, or
  prevention of the core task.
- `P1`: observed or inferred invalid value, broken important workflow,
  misrepresented state, or major operational cost.
- `P2`: observed or inferred material friction or unjustified complexity while a
  workable path remains.
- `EVIDENCE P1`: missing proof blocks a core task, authorization, data safety, or
  central business premise.
- `EVIDENCE P2`: missing proof limits a material conclusion without blocking a
  core or safety claim.

## Output only issues

```text
Issues:
- [P0|P1|P2] [VALUE|SYSTEM|LOGIC|UI|EVIDENCE] `location`
  Issue: ...
  Impact: ...
  Evidence: observed|inferred|missing — ...
```

If the user explicitly requests solutions, add one minimal `Remedy:` line to
each issue; do not add a separate plan or silently invoke Spec or Distill. After
the user accepts or resolves issues, they may explicitly invoke `$craft:spec` or
`$craft:distill` as appropriate.

If no supported material issue or required evidence gap exists, output only:

`No material issues found.`

## Full Loop delegation

When delegated by Full Loop, inspect only the exact delegated Build command
selector, task goal, cited contract content without ledger labels, baseline,
exact task-owned review-handoff diff, and verification evidence. Do not widen
into unrelated ledger items or paths.

Full Loop's delegated request explicitly asks for solutions, so add exactly one
minimal `Remedy:` to each issue. Remain read-only and preserve the exact clean
sentinel above.

---
name: plan
description: >
  Elicit, research, challenge, and expand rough feature ideas or product
  concepts into decision-ready implementation plans. Use only when explicitly
  invoked as $craft:plan with an idea, problem, feature, direction, or proposal
  that needs discovery, clarification, problem decomposition, option analysis,
  or a concrete implementation path. Conduct a multi-turn interview while
  material knowledge remains in the user's head; stay read-only and do not
  write SPEC.md or implement the plan.
---

# Plan

Turn incomplete intent into a shared, evidence-backed model and an executable
path. The user owns product truth. Research owns discoverable facts. Keep every
inference and unresolved choice visible.

## Frame the work

1. Resolve the idea or named artifact from the invocation. Ask one focused
   scope question only when multiple materially different targets remain.
2. When the idea concerns an existing project, resolve its root, read relevant
   local instructions, and inspect the current product flow before interviewing.
3. Treat the conversation as the working record. Default to a planning brief in
   the response; do not create `PLAN.md`, edit another file, or persist
   auxiliary state.
4. Calibrate depth to consequence. A reversible local change needs less
   discovery than a public contract, migration, permission boundary, or costly
   product direction.

Do not confuse the user's first solution with the underlying need. Restate the
initial model as problem, affected actor, desired change, and stated solution;
label missing parts instead of filling them with familiar product patterns.

## Build shared understanding

Track claims in four buckets throughout the conversation:

- `Confirmed`: stated by the user or observed directly in a named artifact;
- `Inferred`: a reasoned interpretation still open to correction;
- `Decided`: a tradeoff the user has chosen with its reason;
- `Open`: an unanswered question, evidence gap, or deferred decision.

Reflect the user's meaning before narrowing it. Use their domain terms and
briefly say what you think they mean, including tensions or contradictions, so
they can correct the model. Never present a polished paraphrase as confirmation.

## Interview for tacit knowledge

Ask the smallest next set of questions with the highest decision value. Use one
to three concise questions per turn, one topic at a time; use one when the
question is difficult or its answer changes the rest of the interview. Summarize
what changed before the next wave.

Choose prompts adaptively:

- Start broad: “If this works, what becomes possible or stops being painful?”
- Recover an episode: “Walk me through the last concrete time this happened.”
- Move upward from a requested feature: “What outcome would that enable?”
- Move downward from an abstraction: “What would a person do or observe?”
- Find boundaries: “When should this deliberately not happen?”
- Find false success: “What could look successful while still being wrong?”
- Contrast cases: ask what differs between an acceptable and unacceptable
  example.
- Expose tradeoffs: offer concrete consequences, then ask which matters more.
- Test the model: give a compact scenario or example and invite correction.

Prefer neutral, open prompts. Avoid leading questions, repeated bare “why,”
double questions, jargon, and questionnaire dumps. If the user is unsure, offer
two or three concrete interpretations as hypotheses, explain their consequences,
and let the user accept, combine, reject, or defer them. Respect “I don't know”;
record it and identify the cheapest way to learn.

Use conversational techniques to improve recall and shared understanding, not
to manipulate agreement. Do not diagnose the user, manufacture urgency, exploit
emotion, or steer them toward the agent's preferred solution.

## Research before asking

Do not ask the user for facts available from the named codebase, artifact, or an
authoritative source. Research only questions that can change the problem model,
available options, constraints, risk, or implementation path.

For an existing system, trace relevant entry points, callers, state ownership,
interfaces, persistence, tests, and documented constraints. Reuse current
capabilities and locate the common ownership point before proposing new parts.

For external research, prefer primary and current authoritative sources. Cite
the sources next to the claims they support, distinguish source fact from
inference, and date facts likely to drift. If required evidence is unavailable,
name the gap and ask whether to proceed with an explicit assumption.

Keep research read-only. Do not install dependencies, start services, change
provider state, run mutating commands, or broaden into unnamed repositories.
Stop when another search is unlikely to change a material decision.

## Decompose the problem

Trace the idea from outcome to implementation without prematurely designing it:

1. Identify the root problem, evidence it exists, affected actors, and current
   workaround or baseline.
2. Define observable success and the smallest useful outcome.
3. Establish in-scope behavior, explicit non-goals, constraints, and trust or
   safety boundaries.
4. Walk the primary scenario and material invalid, empty, unauthorized, stale,
   duplicate, interrupted, concurrent, retried, and partially failed paths when
   relevant.
5. Map authoritative state, transitions, interfaces, side effects, and ownership.
6. Surface dependencies, irreversible choices, operational needs, and rollout
   or recovery requirements proportional to the change.
7. Separate root problems into ordered implementation slices that each produce
   observable value or proof.

Generate alternatives only where a real decision exists. Include the reuse or
no-build option. Compare consequences against confirmed goals and constraints,
recommend the smallest option supported by evidence, and require the user to
own any new product rule. Add no speculative users, scale, integrations,
configurability, or abstraction.

## Close material gaps

Do not declare the plan ready while an unanswered question could materially
change the outcome, actor, scope boundary, data owner, public interface,
authorization, privacy, irreversible migration, or acceptance test. Continue
the interview or stop and name the exact decision or evidence still needed.

Non-material unknowns may remain only when the brief names the assumption, its
risk, who or what can resolve it, and when it must be resolved. If the initial
request already answers the material questions, skip ceremonial interviewing.

Before finalizing a complex or multi-turn plan, present a compact understanding
check and incorporate the user's correction. Do not seek confirmation merely to
repeat a model the user has already explicitly confirmed.

## Deliver the planning brief

Return the smallest self-contained brief that a new implementer could act on
without reading the interview:

```text
# <concept> planning brief

## Intent
Problem: ...
Outcome: ...
Evidence and success: ...

## Actors and scenarios
...

## Scope
In: ...
Out: ...

## Current system and constraints
...

## Decisions
- <decision> — <reason and consequence>

## Proposed behavior and ownership
...

## Implementation path
1. <slice> — <ownership point, interfaces/state, dependencies>

## Verification and delivery
...

## Risks, assumptions, and open items
...
```

Omit headings that genuinely do not apply. Name exact files, interfaces, and
commands only when inspection supports them. Each non-trivial implementation
slice must state its observable completion condition and smallest useful proof.
Include rollout, recovery, observability, migration, accessibility, security,
or performance work only when the feature makes it material.

End with the next explicit boundary: an accepted brief may be passed to
`$craft:spec` for Caveman encoding. Do not invoke Spec automatically, emit
SPEC IDs, edit `SPEC.md`, or imply authorization for `$craft:build`.

## Boundaries

- Read-only conversation and research; no file edits, tests that may mutate,
  staging, commits, pushes, deployments, or provider actions.
- No sub-agents, parallel interviewers, dashboards, or hidden persistent state.
- Preserve exact user terms, source identifiers, paths, commands, and quoted
  language; use ordinary clear English, not Caveman syntax.
- Never hide a material gap behind generic “best practice” or an invented
  assumption.

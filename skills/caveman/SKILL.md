---
name: caveman
description: >
  Encode SPEC.md, invariants, interfaces, tasks, and bug entries with compact,
  precise Caveman syntax. Use for Craft's spec-adjacent writes or explicitly as
  $craft:caveman. Do not apply it to ordinary explanations, code, errors,
  commits, or pull requests.
---

# Caveman

Use this contract as default for `SPEC.md`. If repository root contains
`FORMAT.md`, read it and apply it as stricter local override.

## Grammar

- Drop articles, filler, pleasantries, hedging, and optional auxiliary verbs.
- Use fragments and short imperative verbs when meaning remains exact.
- Preserve code, paths, URLs, identifiers, versions, numbers, error strings,
  SQL, regex, JSON, YAML, and quoted text verbatim.
- Keep any word whose removal loses a fact.

Prefer symbols: `→` leads to, `∴` therefore, `∀` every, `∃` exists, `!`
required, `?` optional or unknown, `⊥` forbidden, `≠` differs, `∈` in, `∉`
not in, `≤`, `≥`, `&`, `|`, `§` section.

## SPEC shape

Keep sections in order:

```text
§G
<one-line goal: what + why>

§C
<constraints>

§I
<kind>: <name> → <shape>

§V
V1: <testable invariant>

§T
id|status|task|cites
T1|.|<task>|V1,I.api

§B
id|date|cause|fix
B1|YYYY-MM-DD|<root cause>|V1,T1
```

Use `.` todo, `~` work in progress, `x` done. Outside a confirmed
`$craft:distill`, keep V/T/B numbering monotonic and never reuse or renumber
identifiers. A confirmed Distill may remove rows and renumber survivors from 1
only while atomically rewriting every citation under its canonical contract.
Keep `§B` append-only between Distill runs. Escape literal `|` as `\|`.
`§T.cites` lists invariant and interface dependencies; `!` may mark a hard
dependency when local `FORMAT.md` permits it.

Use normal English for external prose, commit messages, pull requests, code
comments, and user-requested explanations.

---
name: caveman
description: >
  Encode Craft's SPEC.md and spec-adjacent writes with compact, precise syntax,
  or invoke explicitly as $craft:caveman. Ordinary explanations, code, errors,
  commits, and pull requests keep their normal format.
---

# Caveman

Use this contract as the default for `SPEC.md`, including invariants, interfaces,
tasks, and bug entries. If the repository root contains `FORMAT.md`, read it and
apply it as the stricter local override. Apply the encoding within the current
workflow's authorized writes.

## Grammar

- Drop articles, filler, pleasantries, empty hedging, and optional auxiliary verbs.
- Use fragments and short imperative verbs when meaning remains exact.
- Clarity wins over brevity. Keep conditions and step order unambiguous.
- Use the same term for the same thing; do not rotate synonyms.
- Keep correct grammar when equally concise. Never add words or distort grammar
  merely to sound Caveman.
- Preserve code, paths, URLs, identifiers, versions, numbers, error strings,
  SQL, regex, JSON, YAML, and quoted text verbatim.
- Keep any word whose removal loses a fact or uncertainty. Preserve negation and
  qualifiers such as `not`, `never`, `no`, `only`, and `except`.

Prefer symbols: `→` leads to, `∴` therefore, `∀` every, `∃` exists, `!`
required, `?` optional or unknown, `⊥` forbidden, `≠` differs, `∈` in, `∉`
not in, `≤`, `≥`, `&`, `|`, `§` section.

## SPEC shape

Preserve this section order and row schema:

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

Use `.` todo, `~` work in progress, `x` done. Keep V/T/B numbering monotonic and
never reuse or renumber an identifier. A confirmed `$craft:distill` may remove
rows, but survivors keep the identifiers and citations they already carry, and
removed identifiers leave permanent gaps. Keep `§B` append-only between Distill
runs. Escape literal `|` as `\|`.
`§T.cites` lists invariant and interface dependencies; `!` may mark a hard
dependency when local `FORMAT.md` permits it.

Use normal English for external prose, commit messages, pull requests, code
comments, and user-requested explanations.

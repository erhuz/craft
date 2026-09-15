# SPEC format

This file defines the complete local format for repository-root `SPEC.md`.
It takes precedence over the bundled Caveman format. Craft skills retain their
existing authority over edits, implementation, verification, and compaction.

Use compact English for ledger content. Use normal English for explanations,
external documents, code comments, commits, and pull requests.

## Writing rules

- Remove filler, pleasantries, empty hedging, and dispensable articles or
  auxiliary verbs. Preserve facts, uncertainty, and the strength of requirements.
- Express one idea per sentence or clause. Prefer active voice and direct verbs.
  Use consistent terms; repeat a noun when a pronoun would be ambiguous.
- Retain negation, limits, exceptions, units, and conditions. Words such as
  `not`, `never`, `no`, `only`, and `except` can determine the whole requirement.
- Brevity must not obscure ownership, cause, action order, or failure behavior.
  Use complete sentences when fragments make a rule harder to interpret,
  especially for security requirements and irreversible actions.
- Keep natural grammar when equally concise. Avoid invented abbreviations or
  theatrical broken grammar. Familiar acronyms such as API and HTTP are fine.
- Copy code, commands, paths, URLs, identifiers, environment variables, versions,
  numbers, error strings, SQL, regex, JSON, YAML, and quotations exactly.
  Compression applies only to surrounding prose; keep code spacing and comments.
- Preserve headings, nesting, table fields, and references when shortening text.
  Removing ledger entries belongs to the existing confirmed Distill workflow.

## Sections

Keep these six headings in order, including sections with no entries:

| Heading | Content |
| --- | --- |
| `§G` | One-line outcome: what and why. |
| `§C` | Constraints, assumptions, and explicit non-goals. |
| `§I` | Named interface contracts, actors, data ownership, and side effects. |
| `§V` | Testable behavioral rules, each with a permanent invariant ID. |
| `§T` | Ordered tasks, status, and invariant/interface dependencies. |
| `§B` | Confirmed defect history: date, root cause, fix, and relevant references. |

Write each interface as `<key>: <contract>` and cite it as `I.<key>`.
Write each invariant as `V<n>: <rule>`. Constraints and interface definitions
belong in their own sections; reference them rather than duplicating them.

The following shows syntax; placeholder entries are not project requirements:

```text
§G
<outcome and reason>

§C
- <constraint>

§I
api: <input> → <output and behavior>

§V
V1: <testable behavioral rule>

§T
id|status|task|cites
T1|.|<task>|V1,I.api

§B
id|date|cause|fix
B1|YYYY-MM-DD|<root cause>|V1,T1
```

## Rows and references

- Keep the exact `§T` and `§B` headers shown above. Each row occupies one line
  with four pipe-delimited fields. Empty tables retain their header.
- Escape a literal pipe inside any field as `\|`, including inside code spans.
  A pipe used as a field separator remains unescaped.
- Task status: `.` means todo, `~` means in progress, and `x` means verified done.
  Wording changes alone do not change status.
- Task `cites` contains comma-separated invariant IDs and interface references,
  such as `V1,I.api`. Use plain references; write dependency conditions in prose.
- Bug dates use `YYYY-MM-DD`. The `cause` records the confirmed root cause;
  `fix` describes the correction and may cite relevant invariants, tasks, or
  interfaces. Do not invent a new invariant or task merely to fill this field.
- Allocate `V`, `T`, and `B` numbers independently, above every number previously
  allocated for that prefix. Never reuse or renumber an ID, including removed IDs.
- Confirmed Distill may remove rows. Surviving IDs retain their identities;
  removed IDs leave permanent gaps. Preserve surviving citations and keep all
  retained references valid. Bug history stays append-only between Distill runs.

## Notation

Use these established symbols when the meaning is clear:

`→` leads to; `∴` therefore; `∀` every; `∃` exists; `!` required;
`?` optional or unknown, distinguished by context; `⊥` forbidden;
`≠` differs; `∈` in; `∉` not in; `≤` at most; `≥` at least;
`&` and; `|` or outside table separators; `§` section.

Spell out any relationship that symbols would make ambiguous. Symbols encode
meaning; their use makes no claim about measured token savings.

## Inspiration

The prose rules draw on JuliusBrussee's [Caveman skill](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md)
and its [prose compression safeguards](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman-compress/SKILL.md).
The ledger schema, status notation, and permanent identifiers follow Craft.

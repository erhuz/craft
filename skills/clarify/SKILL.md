---
name: clarify
argument-hint: "[text or artifact]"
description: >
  Clarify technical prose while preserving its meaning and exact literals.
  Apply while drafting or revising technical writing; use $craft:clarify or
  /craft:clarify, or select in the desktop skill menu, for a targeted rewrite.
  Craft loads this guidance at SessionStart.
---

# Clarify

Before applying this guidance, read and apply `../_shared/entry.md`.

Make the meaning explicit before naming the technical concept. Apply to all
technical writing in the current request: explanations, reports, plans,
specifications, documentation, and comments.

## Interface text

Omit microcopy that explains obvious actions or repeats nearby text. Keep text
that helps the user choose, act, recover, or understand a consequence, plus
necessary instructions, accessibility information, constraints, and warnings.
Use direct labels; name states directly and keep color as a visual cue. Use
parentheses only for necessary distinctions or units, and no parenthetical
technical phrases unless the user needs them to act.

## Notice missing meaning

Flag words and sentences that hide who acts, what happens, under which
conditions, or with what result. Interpret each occurrence in its own context;
reuse an explanation only when the meaning matches, not merely the wording.
Use supplied context and available source evidence. If several readings remain,
name the missing information instead of picking one. Words like "robust,"
"efficient," and "safe" can hide missing criteria; a longer synonym does not
fix that. Never invent actors or guarantees.

## Explain first

- Replace opaque wording with `explanation (original technical phrase)`,
  keeping the phrase verbatim.
- Rewrite the whole sentence when substitutions leave action, conditions, or
  consequence unclear; keep only its key technical phrases.
- Keep each original phrase once per distinct meaning per independently
  readable section or audit finding (unsectioned text is one section); use the
  plain explanation afterward.
- Convert suitable `term (explanation)` to explanation-first after checking the
  fit; never reverse parentheses mechanically.
- Leave clarified or already clear text stable: no repeated or nested
  annotations on a second pass, and no invented jargon.

## Preserve exact meaning and protected content

- Keep names, abbreviations, and notation unchanged and undefined: Postgres,
  Redis, Go, Golang, PHP, API, CLI, HA, DCS, `→`, `≠`.
- Keep code, identifiers, commands, paths, URLs, versions, numbers, units,
  error strings, and quoted evidence verbatim; never rename an identifier.
- Preserve responsibility, negation, uncertainty, conditions, exceptions,
  ordering, and evidence strength. Possible stays possible; inferred never
  becomes observed; no narrower guarantee than the context supports.

For contextual examples, read `examples.md` beside this skill before a targeted
rewrite or when unsure.

## Stay within the request

Return the text in its existing structure, reporting unresolved meanings there.
Add a jargon inventory only on request. A review stays a review; edits stay in
the authorized target. A bare invocation with no target asks for the text and
never starts a repository-wide rewrite. Clarify changes wording only, not
requirements, ledger identities, task statuses, edit authority, or other
skills' output structures, and grants no other authorization.

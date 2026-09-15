---
name: clarify
description: >
  Write and revise technical prose with contextual explanations in place of
  opaque jargon and vague sentences. Keep original technical phrases in
  parentheses once per section, while preserving names, abbreviations,
  notation, and exact literals. Apply to all technical writing, including
  explanations, reports, plans, specifications, documentation, and comments.
  Craft loads this guidance at SessionStart; use $craft:clarify for a targeted
  rewrite as well.
---

# Clarify

Make the meaning explicit before naming the technical concept. Apply this
guidance while drafting and editing prose within the current request.

## Notice missing meaning

Read the surrounding text before choosing a replacement. Flag words and
sentences that hide who acts, what happens, which conditions apply, or what
result follows. Terms such as "reconciliation," "persisted," "work admission,"
and "fields have no consumers" are candidates, not a replacement dictionary.
Ordinary uses of "binding" or "fields" may already be clear.

Interpret every occurrence in its own sentence and surrounding context. The
same word can describe different actions, actors, or constraints elsewhere;
do not reuse an earlier explanation merely because the wording matches.
Reuse an explanation only when the meaning also matches. Check supplied
examples against the current context before adapting them.

Use supplied context and relevant available source evidence to establish the
meaning. If several interpretations remain possible, identify the missing
information instead of picking one. "Robust," "efficient," and "safe" can hide
missing criteria; a longer synonym does not resolve that gap. Describe what is
known and flag what remains unclear without inventing actors or guarantees.

## Explain first

- Replace opaque wording with its specific meaning: `explanation (original
  technical phrase)`. Keep the original phrase verbatim.
- Rewrite an entire sentence when word substitutions would leave the action,
  conditions, or consequence unclear. Retain only its key technical phrases
  beside their explanations, never the whole original sentence.
- Retain each original phrase once per distinct meaning in each independently
  readable section or audit finding. Use the plain explanation alone afterward
  for that meaning. If the meaning changes within a section, explain and
  annotate the new meaning too. Unsectioned text counts as one section; use
  consistent wording only where the meaning matches.
- Convert suitable `term (explanation)` wording to explanation-first form after
  checking that the explanation fits the context. Do not reverse parentheses
  mechanically or alter protected content.
- Leave already clarified text stable. Count existing explanation-first pairs
  toward the section's first use; add no nested or repeated annotations on a
  second pass. Leave clear prose alone and never invent jargon to annotate it.

## Preserve exact meaning and protected content

- Keep names, abbreviations, and notation unchanged even when unexplained:
  Postgres, Redis, Go, Golang, PHP, API, CLI, HA, DCS, and symbols such as `→`
  and `≠`. Do not expand them, replace them, or add definitions for them.
  Clarify surrounding prose when needed while keeping these tokens intact.
- Preserve code, identifiers, commands, paths, URLs, versions, numbers, units,
  error strings, and quoted evidence verbatim. Edit explanatory prose around
  them; do not rename an identifier because its name resembles jargon.
- Preserve responsibility, negation, uncertainty, conditions, exceptions,
  ordering, and evidence strength. A possible failure must remain possible;
  an inferred consequence must not become an observed incident. Never replace
  a broad claim with a narrower guarantee unsupported by context.

## Examples

These examples use the stated context. They are not universal definitions.

### Words and short phrases

| Context | Before | After |
| --- | --- | --- |
| The configuration has been saved. | persisted configuration | saved settings (persisted configuration) |
| The manager applies saved settings to running Postgres servers. | reconciliation | applying saved settings to running Postgres servers (reconciliation) |
| A report compares two stock lists to find mismatches. | reconciliation | comparing two stock lists to find mismatches (reconciliation) |
| The manager decides whether another operation may start. | work admission | deciding whether another operation may start (work admission) |
| Different parts report conflicting states for the same servers. | divergent system truth | conflicting reports about the same servers (divergent system truth) |
| The sentence concerns a physical book. | Check the book's binding before shipping it. | Check the book's binding before shipping it. |

The two uses of "reconciliation" need different explanations. Neither
explanation can be carried over to the other context solely because the word
is the same.

### Whole sentences

**Context:** The manager saves settings, but no code uses them to configure
Prometheus.

Before: The fields have no consumers.

After: The manager saves these settings, but no code uses them to configure
Prometheus (fields have no consumers).

**Context:** Applying saved settings can finish successfully while DCS still
uses earlier rules.

Before: Reconciliation can succeed while effective policy remains stale.

After: Applying saved settings (Reconciliation) can succeed while the rules
DCS currently uses (effective policy) still reflect earlier settings.

**Context:** No failure conditions, workloads, or performance criteria are given.

Before: The API is robust and handles load efficiently.

Response: The claim does not specify which failures the API handles, which
workloads it supports, or how performance is measured. Its meaning remains
unclear.

**Protected content:** Leave `Postgres, Redis, Go, Golang, PHP, API, CLI, HA,
DCS; a → b; a ≠ b` unchanged. Their presence alone calls for no explanation.

## Stay within the request

Return the requested text or artifact in its existing structure. Report
unresolved meanings within that output format; do not prepend a jargon
inventory unless requested. A review stays a review, and file edits stay within
the authorized target. A bare invocation with no clear target asks for the text
or artifact to clarify; it never starts a repository-wide rewrite.

Respect document formatting and Craft phase rules. Clarify changes wording,
not requirements, ledger identities, task statuses, or edit authority. Other
skills still own their workflows and output structures. Loading this policy
adds no implementation, audit, or external-action authorization.

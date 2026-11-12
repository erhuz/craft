# Clarify examples

These examples use the stated context. They are not universal definitions.

Terms such as "reconciliation," "persisted," "work admission," and "fields
have no consumers" are candidates, not a replacement dictionary. Ordinary uses
of "binding" or "fields" may already be clear.

### Interface text

Under **Email address**, omit "Enter your email address into this field."
Keep "We'll send your receipt here" when that is accurate and the purpose is
otherwise unclear.

Name the state directly: "Aktivt orderfönster", not "Grön (aktivt fönster)".

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

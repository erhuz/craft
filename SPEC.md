§G
Enforce explicit Craft phase authorization, valid task ownership & compact current-truth reconciliation → prevent unintended writes, stale history, identifier coupling, adoption of user work, or false clean results

§C
- `$craft:spec` owns semantic `SPEC.md` writes only; `$craft:build` or explicit `$craft:full-loop` owns implementation, tests, staging, commit
- `$craft:distill` owns confirmed whole-ledger compaction; `$craft:destill` = explicit compatibility alias
- `$craft:check` evaluates current truth; `§B` history append-only between Distill runs & excluded from drift
- direct Build executes one task at a time; `--all` remains sequential with one verified commit per task
- shared structured semantic-phase action ID unavailable across supported hosts ∴ exact prompt grammar remains routing boundary
- Build-authored implementation artifacts use domain meaning, never volatile SPEC identifiers
- source checkout only; installed plugin/cache refresh requires separate authorization
- no dependency, provider action, deployment, sibling repository, end-to-end agent harness, or broad hook enforcement

§I
skill-policy: `skills/*/agents/openai.yaml` → `policy.allow_implicit_invocation: boolean`
prompt-hook: `UserPromptSubmit` → `additionalContext` / `{"decision":"block","reason":"..."}` / no output
phase-state: `PLUGIN_DATA` or `CLAUDE_PLUGIN_DATA` → `spec-build-gate/<sha256(session_id)>`
phase-authority: `$craft:spec` → SPEC semantics; `$craft:distill` / `$craft:destill` → confirmed SPEC compaction; `$craft:backprop` → explicit or Build-delegated defect flow; `$craft:build` & `$craft:full-loop` → implementation authority
distill-invocation: `$craft:distill` / `$craft:destill` + no arguments → one canonical contract; other scope → `INVALID_SCOPE`
distill-rewrite: stable root `SPEC.md` + current intent + evidence + operator decisions → preview / confirmed atomic replacement / no-op
implementation-artifact: Build-authored source + tests + comments/docstrings + docs + runtime output + commit/handoff prose → domain meaning; SPEC identifiers ⊥
check-scope: `$craft:check` / `--all` → current `§G` + `§C` + `§I` + `§V` + `§T`; `§B` excluded
build-scope: `$craft:build` → no selector / `--next` / `--all` / exactly one `T<n>`; malformed scope → `INVALID_SCOPE`
task-selector: explicit `T<n>` → selected open task / `TASK_NOT_FOUND` / `TASK_ALREADY_COMPLETE` / `TASK_OWNERSHIP_AMBIGUOUS`; `--next` → one ledger task or strict no-op
git-ownership: baseline index/worktree + task-owned diff → exact task commit; unrelated state unchanged

§V
V1: ∀ skill declaring explicit-only invocation, `agents/openai.yaml` contains `policy.allow_implicit_invocation: false`
V2: Pre-Build marker clears only from canonical affirmative `$craft:build` or `$craft:full-loop` invocation; quoted, explanatory, or negated token occurrence ≠ authorization
V3: `UserPromptSubmit` phase-state read/write/delete failure → blocking decision; warning-only exit `0` ⊥
V4: `$craft:spec` raw defect/failure → recommend explicit `$craft:backprop`; internal Backprop or Build transition ⊥
V5: `--next` + one resumable worktree-owned `~` → resume it before any `.`; ambiguous/multiple `~` ownership → stop before mutation; otherwise select lowest-numbered `.`; no `.` or `~` → strict no-op
V6: Build preserves all unrelated baseline bytes & index entries; same-path overlap → stop before mutation or use proven exact task-hunk isolation
V7: `$craft:check` / `--all` evaluates current `§G`, `§C`, `§I`, `§V`, `§T`; `§G`/`§C` → `MATCH`/`DRIFT`/`UNVERIFIABLE`; `§B` excluded; mismatch/evidence gap → `No drift found.` ⊥; legitimate open task alone ≠ drift
V8: direct `$craft:build` accepts no selector, `--next`, `--all`, or exactly one `T<n>`; malformed/mixed/multiple scope → `INVALID_SCOPE` before repository inspection; after `SPEC.md` lookup, unknown ID → `TASK_NOT_FOUND`, `x` → `TASK_ALREADY_COMPLETE`, ambiguous `~` → `TASK_OWNERSHIP_AMBIGUOUS`; rejection/no-op → code inspection, tests, Git-status handling, mutation ⊥
V9: Pre-Build marker sets only when first non-whitespace token = exact lowercase `$craft:plan`, `$craft:spec`, `$craft:distill`, or `$craft:destill`, optionally followed by grammar-valid arguments; quoted, embedded, explanatory, negated, punctuated, or case-changed occurrence ≠ activation; defaults use canonical commands
V10: `$craft:distill` canonical skill documents alias; `$craft:destill` explicit-only alias registration loads canonical contract without duplicated behavior; both exact no-argument commands reach same workflow
V11: Distill requires existing root `SPEC.md`, readable format, no `~` task & no implementation reference to volatile SPEC identifiers; otherwise stop before repository widening or write
V12: Distill first returns evidence-backed keep/rewrite/remove set + complete replacement diff + old→new ID map; implementation mismatch → ask defect / changed intent / unknown; mutually exclusive ledger intent → ask surviving claim / unknown; defect or unknown preserves intent; unanswered semantic choice → confirmation invalid & write ⊥
V13: confirmed Distill preserves current intent, open tasks + cited contracts, trust-boundary/data-loss/security/failure rules & unresolved defects; removes only proven obsolete/duplicate/reverted truth, captured completed tasks & resolved bug history; stable snapshot required; surviving V/T/B rows renumber from 1 with all citations rewritten; only `SPEC.md` changes; no material reduction → `No distillation needed.`
V14: Build-authored implementation artifacts never contain actual SPEC identifiers except exact Craft command selectors; every authored/materially changed non-generated function includes intent + rationale comment/docstring; feature commit = `build: <goal>`; defect commit = `fix: <root cause>`; completion prose omits unnecessary IDs

§T
id|status|task|cites
T1|x|Enforce explicit-only metadata for Full Loop & add regression covering every explicit-only skill|V1,I.skill-policy
T2|x|Resolve prompt-transition option; align router/default prompts & cover affirmative, quoted, explanatory, negated cases|V2,I.prompt-hook,I.phase-state
T3|x|Fail closed on `UserPromptSubmit` phase-state errors & cover unavailable/invalid plugin data|V3,I.prompt-hook,I.phase-state
T4|x|Repair Spec→Backprop delegation contract & add contract proof preserving explicit phase authority|V4,I.phase-authority
T5|x|Unify Build/Full Loop `--next` precedence & add table-driven selector proof|V5,I.task-selector
T6|x|Probe dirty same-path baseline in disposable Git fixture; enforce overlap stop or exact hunk isolation|V6,I.git-ownership
T7|x|Expand Check to current-truth `§G`/`§C`/`§I`/`§V`/`§T`, exclude `§B` & prove clean sentinel rejects drift/evidence gaps|V7,I.check-scope
T8|x|Validate direct Build scope/task state before inspection or mutation, block invalid command-shaped implementation prompts & add table-driven contract proof|V8,I.build-scope,I.task-selector,I.prompt-hook
T9|x|Anchor Plan/Spec activation, align defaults & cover canonical, multiline, quoted, embedded, explanatory, negated, punctuated, case-changed prompts|V9,I.prompt-hook,I.phase-state
T10|x|Add confirmed current-truth Distill workflow, explicit alias, renumbering safeguards & identifier-independent Build artifacts|V9,V10,V11,V12,V13,V14,I.phase-authority,I.distill-invocation,I.distill-rewrite,I.implementation-artifact

§B
id|date|cause|fix

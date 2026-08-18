§G
Enforce explicit Craft phase authorization, deterministic task continuation & compact current-truth reconciliation → prevent unintended writes, stale history, identifier coupling, or false clean results

§C
- `$craft:spec` owns semantic `SPEC.md` writes only; `$craft:build` or explicit `$craft:full-loop` owns implementation, tests, staging, commit
- `$craft:distill` owns confirmed whole-ledger compaction; `$craft:destill` = explicit compatibility alias
- `$craft:check` evaluates current truth; `§B` history append-only between Distill runs & excluded from drift
- Build may select multiple tasks & ledgers; execution remains single-threaded with one verified commit per task
- exact `$craft:build` first token authorizes any following scope; prompt hook does not whitelist or reject its tail
- pre-existing `~` tasks & dirty intended paths remain resumable; ownership attribution or same-path overlap never blocks Build
- shared structured semantic-phase action ID unavailable across supported hosts ∴ exact prompt grammar remains routing boundary
- Build-authored implementation artifacts use domain meaning, never volatile SPEC identifiers
- source checkout only; installed plugin/cache refresh requires separate authorization
- no dependency, provider action, deployment, repository outside explicit Build request, end-to-end agent harness, or broad hook enforcement

§I
skill-policy: `skills/*/agents/openai.yaml` → `policy.allow_implicit_invocation: boolean`
prompt-hook: `UserPromptSubmit` → `additionalContext` / `{"decision":"block","reason":"..."}` / no output
phase-state: `PLUGIN_DATA` or `CLAUDE_PLUGIN_DATA` → `spec-build-gate/<sha256(session_id)>`
phase-authority: `$craft:spec` → SPEC semantics; `$craft:distill` / `$craft:destill` → confirmed SPEC compaction; `$craft:backprop` → explicit or Build-delegated defect flow; `$craft:build` & `$craft:full-loop` → implementation authority
distill-invocation: `$craft:distill` and `$craft:distill --candidate` for candidate mode; `$craft:distill --promote` for promotion; `$craft:destill` exact alias; malformed scope → `INVALID_SCOPE`
distill-rewrite: stable root `SPEC.md` + current intent + evidence + operator decisions → preview / confirmed atomic replacement / no-op
implementation-artifact: Build-authored source + tests + comments/docstrings + docs + runtime output + commit/handoff prose → domain meaning; SPEC identifiers ⊥
check-scope: `$craft:check` / `--all` → current `§G` + `§C` + `§I` + `§V` + `§T`; `§B` excluded
build-request: exact first token `$craft:build` + unrestricted tail → one|many concrete ledgers/tasks; unresolved mapping → focused clarification before mutation
task-selector: one|many explicit task IDs / `--next` / `--all` / request-defined selector clauses → per-ledger ordered tasks / strict no-op / `TASK_NOT_FOUND` / `TASK_ALREADY_COMPLETE`
git-ownership: baseline index/worktree + selected task paths → exact task commit; pre-existing selected-path content preserved; unrelated state unchanged

§V
V1: ∀ skill declaring explicit-only invocation, `agents/openai.yaml` contains `policy.allow_implicit_invocation: false`
V2: Pre-Build marker clears from exact first-token `$craft:build` with any tail or canonical affirmative `$craft:full-loop`; quoted, explanatory, negated, punctuated, or case-changed token occurrence ≠ authorization
V3: `UserPromptSubmit` phase-state read/write/delete failure → blocking decision; warning-only exit `0` ⊥
V4: `$craft:spec` raw defect/failure → recommend explicit `$craft:backprop`; internal Backprop or Build transition ⊥
V5: `--next` + ∃ `~` → resume lowest-numbered `~` before any `.`; otherwise select lowest-numbered `.`; no `.` or `~` → strict no-op; ownership attribution ≠ blocker
V6: Build preserves current staged, unstaged & untracked content; dirty intended path or inseparable same-path baseline ≠ blocker; apply smallest change atop current content; task commit may include preserved same-path baseline; unrelated paths unchanged
V7: `$craft:check` / `--all` evaluates current `§G`, `§C`, `§I`, `§V`, `§T`; `§G`/`§C` → `MATCH`/`DRIFT`/`UNVERIFIABLE`; `§B` excluded; mismatch/evidence gap → `No drift found.` ⊥; legitimate open task alone ≠ drift
V8: exact first-token `$craft:build` authorizes any command tail; prompt hook scope validation/rejection ⊥; Build resolves any concrete combination of task IDs, selectors, paths, ledgers, flags, or natural-language scope through read-only inspection; unresolved materially different mappings → one focused clarification before mutation; missing ledger → `SPEC_MISSING`, unknown ID → `TASK_NOT_FOUND`, `x` → per-task `TASK_ALREADY_COMPLETE`
V9: Pre-Build marker sets only when first non-whitespace token = exact lowercase `$craft:plan`, `$craft:spec`, `$craft:distill`, or `$craft:destill`, optionally followed by grammar-valid arguments; quoted, embedded, explanatory, negated, punctuated, or case-changed occurrence ≠ activation; defaults use canonical commands
V10: `$craft:distill` canonical skill documents candidate and promotion modes; `$craft:destill` remains exact alias registration; promotion mode only with explicit `--promote`
V11: Distill requires existing root `SPEC.md`, readable format, and no task `~`; candidate mode tolerates implementation coupling as migration input, while promotion mode blocks unresolved live coupling before commit.
V12: Distill first returns evidence-backed keep/rewrite/remove list + complete replacement mapping + full candidate mapping document in candidate mode; implementation mismatch → ask defect / changed intent / unknown; mutually exclusive ledger intent → ask surviving claim / unknown; defect or unknown preserves intent; unanswered semantic choice → confirmation invalid & write ⊥
V13: confirmed Distill candidate mode preserves current intent, open tasks + cited contracts, trust-boundary/data-loss/security/failure rules & unresolved defects; no-obvious reduction still yields `No distillation needed.`
V14: Distill promotion may replace `SPEC.md` atomically from `NEW_SPEC.md` only when `NEW_SPEC.md` + `DISTILL_MIGRATION.md` are current and open-task meaning is synchronized; remove artifacts after promotion; `SPEC.md` remains authoritative until then.
V15: Build may read `NEW_SPEC.md` and `DISTILL_MIGRATION.md` during migration cleanup; these artifacts may carry candidate identifiers only while migration is active; final product truth stays in `SPEC.md`.
V16: Build-authored implementation artifacts never contain actual SPEC identifiers except exact Craft command selectors; every authored/materially changed non-generated function includes intent + rationale comment/docstring; feature commit = `build: <goal>`; defect commit = `fix: <root cause>`; completion prose omits unnecessary IDs
V17: multi-ledger/task Build normalizes + deduplicates ledger paths, preflights full requested mapping before mutation, then processes ledgers lexically + tasks in ledger order, single-threaded with one verified commit per task; first blocker/failure stops untouched work without reverting completed commits

§T
id|status|task|cites
T1|x|Enforce explicit-only metadata for Full Loop & add regression covering every explicit-only skill|V1,I.skill-policy
T2|x|Resolve prompt-transition option; align router/default prompts & cover affirmative, quoted, explanatory, negated cases|V2,I.prompt-hook,I.phase-state
T3|x|Fail closed on `UserPromptSubmit` phase-state errors & cover unavailable/invalid plugin data|V3,I.prompt-hook,I.phase-state
T4|x|Repair Spec→Backprop delegation contract & add contract proof preserving explicit phase authority|V4,I.phase-authority
T5|x|Unify Build/Full Loop deterministic `--next` precedence: lowest `~` before lowest `.` & add table-driven selector proof|V5,I.task-selector
T6|x|Preserve dirty same-path baseline, continue task execution & prove unrelated paths remain unchanged|V6,I.git-ownership
T7|x|Expand Check to current-truth `§G`/`§C`/`§I`/`§V`/`§T`, exclude `§B` & prove clean sentinel rejects drift/evidence gaps|V7,I.check-scope
T8|x|Keep direct Build activation explicit, resolve unrestricted request tails read-only & validate task state before mutation|V8,I.build-request,I.task-selector,I.prompt-hook
T9|x|Anchor Plan/Spec activation, align defaults & cover canonical, multiline, quoted, embedded, explanatory, negated, punctuated, case-changed prompts|V9,I.prompt-hook,I.phase-state
T10|x|Add confirmed current-truth Distill workflow, explicit alias, renumbering safeguards & identifier-independent Build artifacts|V9,V10,V11,V12,V13,V14,V15,V16,I.phase-authority,I.distill-invocation,I.distill-rewrite,I.implementation-artifact
T11|x|Remove Build scope whitelist & support deterministic multi-ledger/task execution with prompt-routing proof|V2,V8,V17,I.build-request,I.task-selector,I.prompt-hook

§B
id|date|cause|fix

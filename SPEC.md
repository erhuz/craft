§G
Enforce explicit Craft phase authorization, deterministic task continuation & compact current-truth reconciliation → prevent unintended writes, stale history, or false clean results

§C
- `$craft:spec` owns semantic `SPEC.md` writes only; `$craft:build` owns implementation, tests, staging, commit
- `$craft:distill` owns confirmed whole-ledger compaction; `$craft:destill` = explicit compatibility alias
- `V`/`T`/`B` IDs stable ∀ ledger lifetime; removal leaves permanent gap; renumber or reuse ⊥
- `$craft:check` evaluates ledger-to-code conformance; `$craft:audit` evaluates decision justification; `§B` history append-only between Distill runs & excluded from drift
- Build may select multiple tasks & ledgers; execution remains single-threaded with one verified commit per task
- exact `$craft:build` first token authorizes any following scope; prompt hook does not whitelist or reject its tail
- pre-existing `~` tasks & dirty intended paths remain resumable; ownership attribution or same-path overlap never blocks Build
- explicit skill invocation = phase boundary; prompt-phrase matching, persisted host phase state & natural-language blocklists ⊥ as authorization control
- ID permanent & row content mutable & artifact read without ledger ∴ Build-authored implementation artifacts use domain meaning; SPEC identifiers ⊥ outside `SPEC.md` & exact Craft command selectors; prevention at authorship, accidental reference corrected in final pass, never a stop
- Build-authored code comments and docstrings use English only, regardless of implementation language
- Clarify applies to all technical writing in the current request; it changes wording without changing claims, document structure, or Craft phase authority
- skill output uses bounded sentinel vocabulary
- `§V` holds only checkable behavioral rules; conditions → `§C`; interface shape → `§I`
- source checkout only; installed plugin/cache refresh requires separate authorization
- no dependency, provider action, deployment, repository outside explicit Build request, end-to-end agent harness, or broad hook enforcement

§I
skill-policy: `skills/*/agents/openai.yaml` → `policy.allow_implicit_invocation: boolean`
ponytail-mode: `$craft:ponytail [lite\|full\|ultra]` → conversation-scoped intensity; default `full`; `stop ponytail` / `normal mode` suspends guidance until next activation; activation restores previous or supplied mode; mode/suspension-only request starts no implementation
ponytail-entry: every Build/Backprop/Spec run, direct/delegated/resumed → load sibling Ponytail skill, activate & continue caller workflow; mode rules owned by Ponytail; no added phase authority
session-hook: `SessionStart` → complete Ponytail policy + default `full`, then complete Clarify policy; context limit 12000 characters; known Ponytail mode & suspension survive resume/compaction; no mode storage
clarify-writing: technical words + vague sentences + occurrence-specific context/evidence → plain explanation with original technical phrase once per distinct meaning in each independently readable section/finding; unsectioned text = one section; whole-sentence rewrites retain key phrases only; reuse explanations only when meaning matches; contextual examples ≠ replacement dictionary
clarify-use: automatic guidance for drafting/editing technical prose + `$craft:clarify` targeted rewrite; preserve names, abbreviations, notation, exact literals, quoted evidence & claim meaning; unclear meaning → identify missing context; suitable existing explanations → explanation first; clear or already clarified text → unchanged
prompt-hook: `UserPromptSubmit` → plugin/workflow introduction `additionalContext` on exact trimmed `$craft` / `{"decision":"block","reason":"INVALID_SCOPE: ..."}` on malformed Craft command shape / no output; persisted state ⊥
craft-introduction: bare `$craft` → purpose, `SPEC.md`, explicit Spec → Build → Check steps, getting-started command & current skills discovered from plugin metadata; response only, no tools or skill invocation
phase-authority: `$craft:spec` → SPEC semantics; `$craft:distill` / `$craft:destill` → confirmed SPEC compaction; `$craft:backprop` → explicit or Build-delegated defect flow; `$craft:build` → implementation authority; `$craft:audit` & `$craft:check` → read-only review
distill-invocation: `$craft:distill` sole form; `$craft:destill` exact alias; any argument → `INVALID_SCOPE`
distill-rewrite: stable root `SPEC.md` + current intent + evidence + operator decisions → preview / confirmed atomic `SPEC.md` replacement / no-op; surviving IDs unchanged; staging artifact ⊥
implementation-artifact: Build-authored source + tests + comments/docstrings + docs + runtime output + commit/handoff prose → domain meaning; SPEC identifiers ⊥; comments/docstrings → English only + intent & rationale ∀ authored non-generated function; commit subject `build: <goal>` | `fix: <root cause>`; task diff self-corrected to contract before final verification, never blocked
review: `$craft:audit` → any decision-bearing artifact, ledger optional → `Confirmed` | `Lead` issues; `$craft:check` → `SPEC.md` + code → per-section conformance
sentinel: `SPEC_MISSING` | `FORMAT_MISSING` | `INVALID_SCOPE` | `TASK_NOT_FOUND` | `NO_OPEN_TASKS` + one clean sentinel per skill; other machine token ⊥
check-scope: `$craft:check` / `--all` → current `§G` + `§C` + `§I` + `§V` + `§T`; `§B` excluded
build-request: exact first token `$craft:build` + unrestricted tail → one|many concrete ledgers/tasks; unresolved mapping → focused clarification before mutation
task-selector: one|many explicit task IDs / `--next` / `--all` / request-defined selector clauses → per-ledger ordered tasks / strict no-op / `TASK_NOT_FOUND` / reported already-complete no-op
git-ownership: baseline index/worktree + selected task paths → exact task commit; pre-existing selected-path content preserved; unrelated state unchanged

§V
V1: ∀ skill declaring explicit-only invocation, `agents/openai.yaml` contains `policy.allow_implicit_invocation: false`
V2: exact first-token `$craft:build` authorizes implementation; quoted, explanatory, negated, punctuated, or case-changed occurrence ≠ authorization; no other prompt text grants or withholds it
V3: prompt hook persists no session state; unavailable host plugin data, missing environment, or hook internal error → prompt proceeds unblocked; blocking on absent phase state ⊥
V4: `$craft:spec` raw defect/failure → recommend explicit `$craft:backprop`; internal Backprop or Build transition ⊥
V5: `--next` + ∃ `~` → resume lowest-numbered `~` before any `.`; otherwise select lowest-numbered `.`; no `.` or `~` → strict no-op; ownership attribution ≠ blocker
V6: Build preserves current staged, unstaged & untracked content; dirty intended path or inseparable same-path baseline ≠ blocker; apply smallest change atop current content; task commit may include preserved same-path baseline; unrelated paths unchanged
V7: `$craft:check` / `--all` evaluates current `§G`, `§C`, `§I`, `§V`, `§T`; `§G`/`§C` → `MATCH`/`DRIFT`/`UNVERIFIABLE`; `§B` excluded; mismatch/evidence gap → `No drift found.` ⊥; legitimate open task alone ≠ drift
V8: exact first-token `$craft:build` authorizes any command tail; prompt hook scope validation/rejection ⊥; Build resolves any concrete combination of task IDs, selectors, paths, ledgers, flags, or natural-language scope through read-only inspection; unresolved materially different mappings → one focused clarification before mutation; missing ledger → `SPEC_MISSING`, unknown ID → `TASK_NOT_FOUND`, `x` → per-task reported no-op
V9: `$craft:spec`, `$craft:distill` & `$craft:destill` authorize their own phase only & never imply Build; hook enforces no prompt-phrase blocklist for implementation intent; defaults use canonical commands
V10: `$craft:distill` has one confirmed mode; `--candidate`, `--promote` & staging artifacts ⊥; `$craft:destill` remains exact alias registration
V11: Distill requires existing root `SPEC.md`, readable format & no task `~`; Build self-corrects identifier references at authorship ∴ Distill never blocks on a ledger-ID reference
V12: Distill first returns evidence-backed keep/rewrite/remove list + complete replacement preview; implementation mismatch → ask defect / changed intent / unknown; mutually exclusive ledger intent → ask surviving claim / unknown; defect or unknown preserves intent; unanswered semantic choice → confirmation invalid & write ⊥
V13: confirmed Distill preserves current intent, open tasks + cited contracts, trust-boundary/data-loss/security/failure rules & unresolved defects; no-obvious reduction still yields `No distillation needed.`
V14: confirmed Distill replaces `SPEC.md` atomically in one write; surviving `V`/`T`/`B` keep their IDs; removed IDs leave permanent gaps & are never reallocated; surviving citations unchanged
V15: `SPEC.md` is the sole ledger Build reads; `NEW_SPEC.md` & `DISTILL_MIGRATION.md` ⊥
V16: Build-authored implementation artifacts never contain SPEC identifiers except exact Craft command selectors; every authored/materially changed non-generated function includes intent + rationale comment/docstring, English only, in that language's normal syntax; feature commit = `build: <goal>`; defect commit = `fix: <root cause>`; completion prose omits unnecessary IDs
V17: multi-ledger/task Build normalizes + deduplicates ledger paths, preflights full requested mapping before mutation, then processes ledgers lexically + tasks in ledger order, single-threaded with one verified commit per task; first blocker/failure stops untouched work without reverting completed commits
V18: `§V` admits only a rule falsifiable by one named check; non-falsifiable condition → `§C`; interface shape → `§I` & cited, never restated in `§V`; live `§V` count > 40 → Distill before new `§T`
V20: `$craft:audit` is the sole decision-review skill, accepts any artifact with or without a ledger & separates `Confirmed` from `Lead`; `$craft:check` covers ledger-to-code conformance only
V21: skill machine tokens ⊆ `SPEC_MISSING`, `FORMAT_MISSING`, `INVALID_SCOPE`, `TASK_NOT_FOUND`, `NO_OPEN_TASKS` + one clean sentinel per skill; every other status → plain English
V22: Build authors artifacts without ledger references, then before final verification scans the task-owned diff & rewrites any SPEC identifier outside `SPEC.md` & exact Craft command selectors into domain meaning, running gates on the corrected diff; found reference ≠ blocker, blocked completion ⊥; coincidental `V<n>`/`T<n>` token without reference context ≠ violation
V23: Ponytail mode/suspension changes minimalism & response guidance only; explicit requirements, safety, verification & phase authority unchanged; check: mode/suspension scenarios
V24: SessionStart output includes complete Ponytail body followed by complete Clarify body within configured context limit & declares `full` only as default; check: startup hook regression
V25: Build, Backprop & Spec activate Ponytail before their workflows on every direct/delegated/resumed run, preserving selected mode & phase boundaries; check: phase-entry scenarios
V26: Missing, unreadable, malformed or empty startup policy → diagnostic + retain each successfully loaded policy; all unavailable → diagnostics without injected policy; exit 0; check: startup failure regression
V27: Clarify output satisfies `I.clarify-writing` & `I.clarify-use`, including stable second pass, unchanged protected content & no invented meaning; check: independent behavioral scenarios
V28: prompt hook emits `I.craft-introduction` only for exact trimmed `$craft`; arguments, sub-skills, quoted, embedded, punctuated & case-changed occurrences never trigger introduction; check: bare-invocation regression

§T
id|status|task|cites
T1|x|Enforce explicit-only metadata & add regression covering every explicit-only skill|V1,I.skill-policy
T2|x|Resolve prompt-transition option; align router/default prompts & cover affirmative, quoted, explanatory, negated cases|V2,I.prompt-hook
T3|x|Fail closed on `UserPromptSubmit` phase-state errors & cover unavailable/invalid plugin data|V3,I.prompt-hook
T4|x|Repair Spec→Backprop delegation contract & add contract proof preserving explicit phase authority|V4,I.phase-authority
T5|x|Enforce Build deterministic `--next` precedence: lowest `~` before lowest `.` & add table-driven selector proof|V5,I.task-selector
T6|x|Preserve dirty same-path baseline, continue task execution & prove unrelated paths remain unchanged|V6,I.git-ownership
T7|x|Expand Check to current-truth `§G`/`§C`/`§I`/`§V`/`§T`, exclude `§B` & prove clean sentinel rejects drift/evidence gaps|V7,I.check-scope
T8|x|Keep direct Build activation explicit, resolve unrestricted request tails read-only & validate task state before mutation|V8,I.build-request,I.task-selector,I.prompt-hook
T9|x|Anchor Spec activation, align defaults & cover canonical, multiline, quoted, embedded, explanatory, negated, punctuated, case-changed prompts|V9,I.prompt-hook
T10|x|Add confirmed current-truth Distill workflow, explicit alias, renumbering safeguards & identifier-independent Build artifacts|V9,V10,V11,V12,V13,V14,V15,V16,I.phase-authority,I.distill-invocation,I.distill-rewrite,I.implementation-artifact
T11|x|Remove Build scope whitelist & support deterministic multi-ledger/task execution with prompt-routing proof|V2,V8,V17,I.build-request,I.task-selector,I.prompt-hook
T12|x|Make Build code-comment language explicitly English-only & add contract proof|V16,I.implementation-artifact
T13|x|Make ledger IDs permanent: gaps on removal, no renumber, one confirmed Distill mode; drop candidate/promote, staging artifacts & the ID-reference scanner|V10,V11,V12,V13,V14,V15,I.distill-invocation,I.distill-rewrite
T14|x|Self-correct accidental ledger references in the task diff before final verification & restate the artifact rationale for permanent identifiers|V16,V22,I.implementation-artifact
T15|x|Reduce the sentinel vocabulary to the allowed set|V21,I.sentinel
T16|x|Remove prompt-phrase gating & persisted phase state; never block a prompt on unavailable host plugin data|V2,V3,V9,I.prompt-hook
T19|.|Separate `Confirmed` findings from `Lead` candidates in Audit as the sole decision-review skill|V20,I.review
T20|.|Add `§V` admission criteria & cap enforcement to Spec|V18
T21|x|Remove all-in, full-loop, plan & critique skills, discovery/default entries, delegation paths & obsolete loop contracts; preserve remaining prompt behavior|V1,V8,V9,I.skill-policy,I.phase-authority,I.prompt-hook
T22|x|Add Ponytail modes, preserve conversation selection on policy reload & verify unchanged scope/verification boundaries|V23,V24,I.ponytail-mode,I.session-hook,I.skill-policy
T23|x|Add Ponytail suspension/reactivation, stop alternative research once uncertainty is resolved & prefer correct edge-case handling between equally small solutions|V23,V24,I.ponytail-mode,I.session-hook
T24|x|Activate Ponytail on every Build, Backprop & Spec run through shared activation rules; preserve selected mode & caller workflow|V23,V24,V25,I.ponytail-mode,I.ponytail-entry,I.phase-authority
T25|x|Add Clarify with contextual word/sentence examples, automatic discovery & session loading; verify complete policies, partial failures & writing behavior|V24,V26,V27,I.skill-policy,I.session-hook,I.clarify-writing,I.clarify-use
T26|x|Adapt each Clarify explanation to its occurrence; distinguish meanings of the same phrase within a section & add contrasting examples|V24,V27,I.clarify-writing
T27|x|Replace bare Craft inventory with plugin/workflow introduction, preserve exact invocation routing & align README|V28,I.prompt-hook,I.craft-introduction

§B
id|date|cause|fix

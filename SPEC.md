§G
Enforce explicit Craft phase authorization & single-task ownership → prevent unintended writes, commits, or adoption of user work

§C
- `$craft:spec` owns semantic `SPEC.md` writes only; `$craft:build` or explicit `$craft:full-loop` owns implementation, tests, staging, commit
- confirmed: `IMPLEMENTATION_INVOCATION.search(prompt)` treats discussion/denial as Build authorization & clears session marker
- confirmed: `skills/full-loop/agents/openai.yaml` omits `policy.allow_implicit_invocation: false` despite explicit-only contract
- confirmed: Spec raw-defect dispatch invokes Backprop outside Backprop trigger contract; Backprop may continue into Build
- confirmed: `UserPromptSubmit` state exceptions return `systemMessage` + exit `0` without blocking
- confirmed: Build & Full Loop `--next` prioritize `.` before resumable `~`, conflicting with single-task rule
- ? Direct Build same-path baseline preservation unproven; path staging may adopt unrelated hunks
- ? prompt-transition solution: structured host action ID if verified for Codex & Claude Code; otherwise canonical anchored invocation grammar + aligned default prompts
- ? same-path solution: pre-mutation overlap stop vs deterministic task-hunk isolation; require disposable Git proof
- no dependency, provider action, deployment, sibling repository, or broad hook enforcement

§I
skill-policy: `skills/*/agents/openai.yaml` → `policy.allow_implicit_invocation: boolean`
prompt-hook: `UserPromptSubmit` → `additionalContext` / `{"decision":"block","reason":"..."}` / no output
phase-state: `PLUGIN_DATA` or `CLAUDE_PLUGIN_DATA` → `spec-build-gate/<sha256(session_id)>`
phase-authority: `$craft:spec` → SPEC semantics; `$craft:backprop` → explicit or Build-delegated defect flow; `$craft:build` & `$craft:full-loop` → implementation authority
task-selector: `$craft:build --next` & `$craft:full-loop --next` → one ledger task or strict no-op
git-ownership: baseline index/worktree + task-owned diff → exact task commit; unrelated state unchanged

§V
V1: ∀ skill declaring explicit-only invocation, `agents/openai.yaml` contains `policy.allow_implicit_invocation: false`
V2: Pre-Build marker clears only from canonical affirmative `$craft:build` or `$craft:full-loop` invocation; quoted, explanatory, or negated token occurrence ≠ authorization
V3: `UserPromptSubmit` phase-state read/write/delete failure → blocking decision; warning-only exit `0` ⊥
V4: `$craft:spec` raw defect/failure → recommend explicit `$craft:backprop`; internal Backprop or Build transition ⊥
V5: `--next` + one resumable worktree-owned `~` → resume it before any `.`; ambiguous/multiple `~` ownership → stop before mutation; otherwise select lowest-numbered `.`; no `.` or `~` → strict no-op
V6: Build preserves all unrelated baseline bytes & index entries; same-path overlap → stop before mutation or use proven exact task-hunk isolation

§T
id|status|task|cites
T1|x|Enforce explicit-only metadata for Full Loop & add regression covering every explicit-only skill|V1,I.skill-policy
T2|x|Resolve prompt-transition option; align router/default prompts & cover affirmative, quoted, explanatory, negated cases|V2,I.prompt-hook,I.phase-state
T3|x|Fail closed on `UserPromptSubmit` phase-state errors & cover unavailable/invalid plugin data|V3,I.prompt-hook,I.phase-state
T4|x|Repair Spec→Backprop delegation contract & add contract proof preserving explicit phase authority|V4,I.phase-authority
T5|x|Unify Build/Full Loop `--next` precedence & add table-driven selector proof|V5,I.task-selector
T6|x|Probe dirty same-path baseline in disposable Git fixture; enforce overlap stop or exact hunk isolation|V6,I.git-ownership

§B
id|date|cause|fix

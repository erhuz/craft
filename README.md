<p align="center">
  <img src="assets/craft-beaver.png" alt="Craft's beaver mascot, standing with folded arms and a white outline" width="240">
</p>

# Craft

**Specify clearly. Build minimally. Verify deliberately.**

Craft is a workflow plugin for Codex and Claude Code that turns software changes into compact specifications, verified implementation, and lessons from confirmed defects.

Coding agents can move quickly from an idea to code while leaving intent, scope, and completion unclear. Craft gives each phase a defined job and keeps the project's intended behavior and remaining work in `SPEC.md`.

## Installation

### Prerequisites

- Codex with `codex plugin` support, or a version of Claude Code with plugin support.
- `python3` available on `PATH` for the bundled hooks. The hooks use only the Python standard library.
- Git and the tools needed to test and build the project you work on.

### Codex

Run these commands in your terminal:

```sh
codex plugin marketplace add erhuz/craft
codex plugin add craft@erhuz
```

Start a new Codex session in the project where you want to use Craft. Review and trust Craft's hooks when the host requests it; the startup guidance and command catalog depend on those hooks. See the [official plugin guide](https://learn.chatgpt.com/docs/plugins) for host setup, and `codex plugin --help` for the CLI available in your installation.

### Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add erhuz/craft
/plugin install craft@erhuz
/reload-plugins
```

Start a new session in your project so Craft's startup hook also runs. See the [official plugin installation guide](https://code.claude.com/docs/en/discover-plugins) for installation scopes and troubleshooting.

### Verify installation

Send this as a message to your coding agent:

```text
$craft
```

Craft should list its available skills and hooks. The `$craft` and `$craft:...` examples below are agent prompts, not shell commands.

## Quick start

This example starts in a small task-list application's repository without an existing `SPEC.md`. Send each prompt separately and review the result before moving to the next phase.

**1. Describe the change and create its specification.**

```text
$craft:spec Add a completed-task filter to the task list. Keep the current layout and require the existing checks to pass.
```

Spec writes the intended behavior and implementation tasks to `SPEC.md`. Review that file before building.

**2. Build the next task.**

```text
$craft:build --next
```

Build implements one task, runs the applicable checks, and creates a scoped commit when verification passes. Repeat for additional tasks, or use `$craft:build --all` to process all open tasks in order.

**3. Check the result against the specification.**

```text
$craft:check
```

Check reports mismatches and missing evidence without changing files. Writing a specification does not automatically start Build.

For an existing project without a ledger, `$craft:spec from-code` first captures its current behavior. When a ledger already exists, use `$craft:spec amend <section>` with your requested change, then review the task list and select your intended task with `$craft:build <task-id>`. `--next` follows ledger order and may resume earlier work instead of the change you just described.

## Skills reference

### Main workflow

| Skill and command | What it does / when to use it | What it can change |
| --- | --- | --- |
| [Spec](skills/spec/SKILL.md) · `$craft:spec` | Define a new change, capture current behavior, or amend the project's intended behavior. | The meaning and content of repository-root `SPEC.md`. |
| [Build](skills/build/SKILL.md) · `$craft:build --next` | Implement and verify specified work. Also accepts `--all` or explicit task scope. | Implementation, tests, task statuses, staging, and scoped commits. |
| [Check](skills/check/SKILL.md) · `$craft:check` | Find where the current specification and code disagree, or where evidence is missing. | Nothing; read-only. |
| [Audit](skills/audit/SKILL.md) · `$craft:audit` | Review whether decisions in code, a proposal, a workflow, or another artifact are justified. A ledger is optional. | Nothing; read-only. |
| [Backprop](skills/backprop/SKILL.md) · `$craft:backprop` | Trace a confirmed defect and propose what the project needs to learn from it. | After confirmation, coordinates Spec and Build through a verified fix and commit. |
| [Distill](skills/distill/SKILL.md) · `$craft:distill` | Reduce an existing ledger to current intent and open work when it has accumulated obsolete or duplicate material. | Replaces `SPEC.md` only after an evidence-backed preview and explicit confirmation. |

`$craft:destill` is a [compatibility alias](skills/destill/SKILL.md) for `$craft:distill`. Neither spelling accepts arguments.

### Supporting skills

| Skill and command | What it does / when to use it | What it can change |
| --- | --- | --- |
| [Ponytail](skills/ponytail/SKILL.md) · `$craft:ponytail` | Choose the smallest correct solution. Select `lite`, `full`, or `ultra`; the default is `full`. | Guidance for the current work; does not authorize a new phase. |
| [Caveman](skills/caveman/SKILL.md) · `$craft:caveman` | Write compact, precise specification text while retaining facts and conditions. | Wording and encoding within the current phase's authorized scope. |
| [Clarify](skills/clarify/SKILL.md) · `$craft:clarify` | Explain technical prose in plain language while preserving exact meaning and literals. | The requested prose; does not change requirements or phase authority. |

The startup hook loads Ponytail and Clarify guidance automatically. Build, Backprop, and Spec also activate Ponytail when they run. `stop ponytail` or `normal mode` suspends its guidance until the next activation; an existing mode choice survives reloads.

## How the workflow works

### One project ledger

`SPEC.md` records what the project should do and what work remains:

| Section | Holds |
| --- | --- |
| `§G` | The goal and why it matters. |
| `§C` | Constraints and explicit non-goals. |
| `§I` | Interfaces, ownership, and side effects. |
| `§V` | Behavioral rules that can be checked. |
| `§T` | Ordered implementation tasks and their dependencies. |
| `§B` | Confirmed defects, their causes, and fixes. |

A project's root `FORMAT.md` takes precedence over the default [Caveman format](skills/caveman/SKILL.md). Ledger identifiers stay stable; removing a row leaves a permanent gap.

### Explicit phases

Spec owns the meaning of the ledger. Build owns implementation and may directly change only task status cells in `SPEC.md`. Check and Audit report evidence without editing. Distill requires confirmation of its complete replacement preview.

Invoke the phase you want explicitly. Review and specification work do not silently become implementation. These are instructions followed by the agent; the prompt hook renders the catalog and validates Distill command shape, rather than enforcing a permissions system.

### Verified tasks and commits

Build moves each task through `.` (open) → `~` (in progress) → `x` (complete). With `--next`, it resumes the lowest-numbered in-progress task before starting an open one.

For each task, Build traces the affected behavior, makes the smallest correct change, and runs focused verification plus the project's required checks. It marks the task complete and commits its scoped changes only after those checks pass. Multiple tasks run sequentially, with one verified commit per task.

Existing work is preserved, including changes already present in a selected task's files. Unrelated paths stay unchanged. A blocker stops the remaining work without rolling back tasks already committed. A local commit does not imply a push or deployment.

### Learning from defects

If an uncommitted implementation violates an already-correct specification, Build fixes it within the current task. When a defect reveals missing or wrong product knowledge, Backprop traces the root cause and proposes a specification correction. After you confirm that proposal, it coordinates Spec and Build through the fix and verification.

Distill later removes proven obsolete or duplicate ledger material while preserving current intent, open work, and unresolved defects. Current code alone does not redefine what the product should do.

## Design principles

- **Build only what is needed.** Reuse existing behavior and standard tools before adding code, dependencies, or abstractions.
- **Keep meaning explicit.** Explain who acts, what happens, and under which conditions. Preserve exact technical literals.
- **Be compact without losing facts.** Short specifications still retain ownership, ordering, exceptions, and uncertainty.
- **Support conclusions with evidence.** Trace causes, distinguish inference from observation, and report missing proof instead of claiming success.
- **Keep the user in control of scope.** Minimalism never removes required verification, failure handling, or an explicit phase boundary.

## Development and contributing

Craft consists of skill instructions, plugin metadata, and small Python hooks:

```text
skills/                    Skill instructions and Codex discovery metadata
hooks/session_start.py     Loads Ponytail and Clarify at session startup
hooks/spec_build_gate.py   Renders the catalog and validates Distill syntax
hooks/hooks.json           Registers hook events and commands
hooks/test_spec_build_gate.py
                           Regression checks for hooks and workflow contracts
.codex-plugin/plugin.json  Codex plugin manifest
.claude-plugin/            Claude Code manifest and marketplace catalog
SPEC.md                   Craft's own specification and task ledger
FORMAT.md                 Local specification format
assets/                   README artwork
THIRD_PARTY_LICENSES/      Third-party notices
```

Run the existing regression suite from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hooks -p 'test_*.py' -v
git diff --check
```

The suite uses Python's standard library. It checks hook behavior and selected instruction contracts; it is not an end-to-end test of an agent following every skill.

For contributions, inspect the relevant skill, hook, and ledger rules together. Keep changes focused, add a regression when behavior changes, and keep manifests and discovery metadata consistent. Describe the affected behavior and your validation in the pull request.

Editing this checkout does not update an installed plugin. Refresh or reinstall it through your host and start a new session when testing installed behavior.

## License and attribution

Craft is maintained by Benjamin Fransson. This repository currently has no project-wide license file.

Craft's Ponytail policy is adapted from [Ponytail](https://github.com/DietrichGebert/ponytail), version 4.8.4, by DietrichGebert. Its MIT license and upstream commit are preserved in [the third-party notice](THIRD_PARTY_LICENSES/ponytail.txt); that notice applies to the attributed material.

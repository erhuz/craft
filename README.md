<a id="top"></a>

<p align="center">
  <img src="assets/craft-beaver.png" alt="Craft's beaver mascot, standing with folded arms and a white outline" width="240">
</p>

<h1 align="center">🦫 Craft</h1>

<p align="center">
  <strong>Specify clearly. Build minimally. Verify deliberately.</strong>
</p>

<p align="center">
  <a href="#-codex"><img src="https://img.shields.io/badge/Codex-plugin-0B4B38?style=flat-square" alt="Codex plugin"></a>
  <a href="#-claude-code"><img src="https://img.shields.io/badge/Claude_Code-plugin-0B4B38?style=flat-square" alt="Claude Code plugin"></a>
</p>

Craft is a workflow plugin for Codex and Claude Code that turns software changes into compact specifications, verified implementation, and lessons from confirmed defects.

Coding agents can move quickly from an idea to code while leaving intent, scope, and completion unclear. Craft makes each part explicit:

- **Know what to build.** Keep intended behavior and remaining work in `SPEC.md`.
- **Finish in verified steps.** Implement one task at a time, run the required checks, and commit the result.
- **Keep what you learn.** Feed confirmed defects back into the specification and remove proven obsolete material.

## 📑 Contents

- [Installation](#-installation)
- [Quick start](#-quick-start)
- [Skills reference](#-skills-reference)
- [How the workflow works](#-how-the-workflow-works)
- [Design principles](#-design-principles)
- [Development and contributing](#-development-and-contributing)
- [License and attribution](#-license-and-attribution)

## 📦 Installation

### 📋 Prerequisites

- Codex with `codex plugin` support, or a version of Claude Code with plugin support.
- `python3` available on `PATH` for the bundled hooks. The hooks use only the Python standard library.
- Git and the tools needed to test and build the project you work on.

### 🤖 Codex

Run these commands in your terminal:

```sh
codex plugin marketplace add erhuz/craft
codex plugin add craft@erhuz
```

Start a new Codex session in the project where you want to use Craft. Review and trust Craft's hooks when the host requests it; the startup guidance and command catalog depend on those hooks. See the [official plugin guide](https://learn.chatgpt.com/docs/plugins) for host setup, and `codex plugin --help` for the CLI available in your installation.

### 💬 Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add erhuz/craft
/plugin install craft@erhuz
/reload-plugins
```

Start a new session in your project so Craft's startup hook also runs. See the [official plugin installation guide](https://code.claude.com/docs/en/discover-plugins) for installation scopes and troubleshooting.

### ✅ Verify installation

Send this as a message to your coding agent:

```text
$craft
```

Craft should list its available skills and hooks.

> [!TIP]
> Send `$craft` and `$craft:...` examples as messages to your coding agent. Run the installation commands in the terminal or Claude Code as indicated above.

## 🚀 Quick start

This example starts in a small task-list application's repository without an existing `SPEC.md`. Send each prompt separately and review the result before moving to the next phase.

> [!NOTE]
> For an existing project without a ledger, `$craft:spec from-code` first captures its current behavior. If `SPEC.md` already exists, use `$craft:spec amend <section>` with your requested change, then select the intended task with `$craft:build <task-id>`. `--next` may resume earlier work instead of the change you just described.

**1. Describe the change and create its specification.**

```text
$craft:spec Add a completed-task filter to the task list. Keep the current layout and require the existing checks to pass.
```

Spec writes the intended behavior and implementation tasks to `SPEC.md`. Review that file before building.

**2. Build the next task.**

```text
$craft:build --next
```

Build implements one task and runs the applicable checks. Repeat for additional tasks, or use `$craft:build --all` to process all open tasks in order.

> [!IMPORTANT]
> Build creates a scoped local commit when verification passes. Review the specification before invoking it; writing a specification does not automatically start Build.

**3. Check the result against the specification.**

```text
$craft:check
```

Check reports mismatches and missing evidence without changing files.

## 🧰 Skills reference

### 🔧 Main workflow

| Skill / command | Use it for | Changes |
| --- | --- | --- |
| [Spec](skills/spec/SKILL.md)<br>`$craft:spec` | Define a change, capture current behavior, or amend intended behavior. | The meaning and content of repository-root `SPEC.md`. |
| [Build](skills/build/SKILL.md)<br>`$craft:build --next` | Implement and verify specified work. Also accepts `--all` or explicit task scope. | Implementation, tests, task statuses, staging, and scoped commits. |
| [Check](skills/check/SKILL.md)<br>`$craft:check` | Find disagreements between the current specification and code, or missing evidence. | Nothing; read-only. |
| [Audit](skills/audit/SKILL.md)<br>`$craft:audit` | Review whether decisions in an artifact are justified. A ledger is optional. | Nothing; read-only. |
| [Backprop](skills/backprop/SKILL.md)<br>`$craft:backprop` | Trace a confirmed defect and propose what the project needs to learn. | After confirmation, coordinates Spec and Build through a verified fix and commit. |
| [Distill](skills/distill/SKILL.md)<br>`$craft:distill` | Reduce a ledger to current intent and open work when obsolete or duplicate material accumulates. | Replaces `SPEC.md` only after an evidence-backed preview and explicit confirmation. |

`$craft:destill` is a [compatibility alias](skills/destill/SKILL.md) for `$craft:distill`. Neither spelling accepts arguments.

### 🧩 Supporting skills

| Skill / command | Use it for | Changes |
| --- | --- | --- |
| [Ponytail](skills/ponytail/SKILL.md)<br>`$craft:ponytail` | Choose the smallest correct solution. Select `lite`, `full`, or `ultra`; the default is `full`. | Guidance for the current work; does not authorize a new phase. |
| [Caveman](skills/caveman/SKILL.md)<br>`$craft:caveman` | Write compact specifications while retaining facts and conditions. | Wording and encoding within the current phase's authorized scope. |
| [Clarify](skills/clarify/SKILL.md)<br>`$craft:clarify` | Explain technical prose while preserving exact meaning and literals. | The requested prose; does not change requirements or phase authority. |

The startup hook loads Ponytail and Clarify guidance automatically. Build, Backprop, and Spec also activate Ponytail when they run. `stop ponytail` or `normal mode` suspends its guidance until the next activation; an existing mode choice survives reloads.

## 🔄 How the workflow works

### 📘 One project ledger

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

### 🚦 Explicit phases

Spec owns the meaning of the ledger. Build owns implementation and may directly change only task status cells in `SPEC.md`. Check and Audit report evidence without editing. Distill requires confirmation of its complete replacement preview.

Invoke the phase you want explicitly. Review and specification work do not silently become implementation. These are instructions followed by the agent; the prompt hook renders the catalog and validates Distill command shape, rather than enforcing a permissions system.

### ✅ Verified tasks and commits

Build moves each task through `.` (open) → `~` (in progress) → `x` (complete). With `--next`, it resumes the lowest-numbered in-progress task before starting an open one.

For each task, Build traces the affected behavior, makes the smallest correct change, and runs focused verification plus the project's required checks. It marks the task complete and commits its scoped changes only after those checks pass. Multiple tasks run sequentially, with one verified commit per task.

Existing work is preserved, including changes already present in a selected task's files. Unrelated paths stay unchanged. A blocker stops the remaining work without rolling back tasks already committed. A local commit does not imply a push or deployment.

### 🔍 Learning from defects

If an uncommitted implementation violates an already-correct specification, Build fixes it within the current task. When a defect reveals missing or wrong product knowledge, Backprop traces the root cause and proposes a specification correction. After you confirm that proposal, it coordinates Spec and Build through the fix and verification.

Distill later removes proven obsolete or duplicate ledger material while preserving current intent, open work, and unresolved defects. Current code alone does not redefine what the product should do.

## 💡 Design principles

- **Build only what is needed.** Reuse existing behavior and standard tools before adding code, dependencies, or abstractions.
- **Keep meaning explicit.** Explain who acts, what happens, and under which conditions. Preserve exact technical literals.
- **Be compact without losing facts.** Short specifications still retain ownership, ordering, exceptions, and uncertainty.
- **Support conclusions with evidence.** Trace causes, distinguish inference from observation, and report missing proof instead of claiming success.
- **Keep the user in control of scope.** Minimalism never removes required verification, failure handling, or an explicit phase boundary.

## 🤝 Development and contributing

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

## 📜 License and attribution

Craft is maintained by Benjamin Fransson. This repository currently has no project-wide license file.

Craft's Ponytail policy is adapted from [Ponytail](https://github.com/DietrichGebert/ponytail), version 4.8.4, by DietrichGebert. Its MIT license and upstream commit are preserved in [the third-party notice](THIRD_PARTY_LICENSES/ponytail.txt); that notice applies to the attributed material.

[↑ Back to top](#top)

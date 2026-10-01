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
  <a href="#-hermes-agent"><img src="https://img.shields.io/badge/Hermes_Agent-plugin-0B4B38?style=flat-square" alt="Hermes Agent plugin"></a>
  <a href="#-claude-desktop"><img src="https://img.shields.io/badge/Claude_Desktop-plugin-0B4B38?style=flat-square" alt="Claude Desktop plugin"></a>
</p>

Craft is a workflow plugin for Codex, Claude, and Hermes Agent that turns software changes into compact specifications, verified implementation, and lessons from confirmed defects. Repository workflows run in Codex Desktop, Claude Desktop's Code tab, and Cowork sessions with the necessary file and command access. Help, writing guidance, and review of supplied artifacts also work in Claude Chat.

Coding agents can move quickly from an idea to code while leaving intent, scope, and completion unclear. Craft makes each part explicit:

- **Know what to build.** Keep intended behavior and remaining work in `SPEC.md`.
- **Finish in verified steps.** Implement one task at a time, run the required checks, and commit the result.
- **Keep what you learn.** Feed confirmed defects back into the specification and remove proven obsolete material.

## 📑 Contents

- [Installation](#-installation)
- [Desktop support](#-desktop-support)
- [Quick start](#-quick-start)
- [Skills reference](#-skills-reference)
- [How the workflow works](#-how-the-workflow-works)
- [Design principles](#-design-principles)
- [Development and contributing](#-development-and-contributing)
- [License and attribution](#-license-and-attribution)

## 📦 Installation

### 📋 Prerequisites

- A current client supporting plugins and the documented hook features, or Hermes Agent with native plugin support.
- For Claude hooks: `python3` on `PATH`, including a real executable on Windows. For Codex hooks: `python3` on Unix, or PowerShell and the Windows Python launcher `py -3` on Windows. The scripts use only the Python standard library.
- For repository workflows: access to the intended repository and required commands. Build also needs Git and the project's verification tools.

Help and supplied-text guidance require no Python, Git, or repository access. If hooks are unavailable, skill entry loads missing Ponytail and Clarify guidance from bundled files. Successfully loaded guidance and the selected Ponytail mode or suspension are retained.

### 🤖 Codex

For Codex Desktop, register the marketplace from a terminal on the computer running the app:

```sh
codex plugin marketplace add erhuz/craft
```

Restart the app, open **Plugins**, choose the `erhuz` marketplace, and install Craft. To test this checkout before its changes reach the marketplace, register its absolute local directory instead: `codex plugin marketplace add /absolute/path/to/craft`. The existing `.claude-plugin/marketplace.json` is supported by the desktop client. See [OpenAI's marketplace guide](https://developers.openai.com/plugins/build/plugins#how-local-marketplaces-work).

You can also install from the terminal with `codex plugin add craft@erhuz`. Start a new chat in your project and review Craft's hooks when the host requests trust. The app loads its installed copy; editing the checkout alone does not refresh it. See the [official plugin guide](https://learn.chatgpt.com/docs/plugins) and `codex plugin --help`.

### 💬 Claude Desktop

Open **Customize > Plugins**, choose **Add > Add marketplace**, enter `erhuz/craft`, then add Craft. To test a source build before publication, choose **Add > Upload plugin** and select the ZIP described below. It contains one `.claude-plugin/plugin.json`. See [Claude's plugin installation guide](https://claude.com/docs/plugins/overview#find-and-add-a-plugin).

This installs Craft on your account for the current organization. Use Help in Chat, grant repository access for Cowork, or open a project in the Code tab. Account plugins sync into new Claude Code sessions; CLI installations stay on their machine. See [Claude's installation and sync table](https://claude.com/docs/plugins/platform-support#compare-installation-sync-and-admin-controls).

### 💬 Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add erhuz/craft
/plugin install craft@erhuz
/reload-plugins
```

Start a new session in your project so Craft's startup hook also runs. These are machine-local installations, including project or local scopes; they do not install Craft into your Claude account. See the [official CLI plugin installation guide](https://code.claude.com/docs/en/discover-plugins) for scopes and troubleshooting.

### ☤ Hermes Agent

Run these commands in your terminal:

```sh
hermes plugins install erhuz/craft
hermes plugins enable craft
```

Start a new Hermes session in your project. Send `$craft` or `$craft:...` as a regular chat message; Hermes loads the corresponding namespaced skill through Craft's prompt hook. Hermes also exposes the bundled skills to its `skill_view` tool under names such as `craft:spec`. See the [Hermes plugin guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md) for installation and activation details.

### ✅ Verify installation

Start a new chat or session and explicitly choose Craft's Help skill in the message box, or send the command for your client:

```text
$craft:help
/craft:help
```

Use `$craft:help` in Codex and `/craft:help` in Claude. Help explains Spec → Build → Check and lists the current installed skills without starting a phase. Check the installed version is `0.2.5` and Help appears in the skill menu. With trusted hooks, legacy bare `$craft` also returns that introduction; in hookless Chat, use Help.

### 🔄 Refresh an installed copy

- **Codex:** for a Git marketplace, run `codex plugin marketplace upgrade erhuz`, then refresh or reinstall Craft in Plugins and restart the app. For a local marketplace, reinstall from the updated local source and restart. Verify the installed version and Help menu entry again.
- **Claude account:** use **Check for updates** for the marketplace in Customize > Plugins; start a new Chat or Cowork session after the update syncs. For an uploaded build, upload the new ZIP through the same installation route. See [Claude's update guidance](https://claude.com/docs/plugins/overview#manage-installed-plugins).
- **Claude Code CLI:** run `claude plugin update craft@erhuz`, then restart the session. `/reload-plugins` reloads available components; use a new session to exercise SessionStart.

Installed-plugin refresh and public directory submission are separate operator actions. A source change or locally prepared ZIP performs neither.

> [!TIP]
> Send one skill command per message. The `$craft:...` examples below use Codex spelling; `/craft:...` invokes the same skill in Claude. Explicit selection of the installed skill in the desktop menu also counts. Reading or quoting a command does not start a phase.

## 🖥️ Desktop support

| Client or mode | Craft workflows | Hooks | Required access |
| --- | --- | --- | --- |
| Codex Desktop / CLI | Full repository workflow, Help, and writing guidance. | Supported when enabled and trusted. | Intended repository files, required commands, and Git for Build. |
| Claude Code / Desktop Code tab | Full repository workflow, Help, and writing guidance. | Supported. | Intended repository files, required commands, and Git for Build. |
| Claude Desktop Cowork | Full repository workflow when the session has the required tools; Help and supplied-artifact review otherwise. | Supported. | Granted repository directory, required commands, and Git for Build. |
| Claude Chat | Help, writing guidance, Audit and Clarify of supplied artifacts. | Ignored by the host. | Bundled resources and the supplied artifacts. |

Claude's component support is documented in its [platform table](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app). Craft checks access before repository operations. An inaccessible repository is an evidence gap; it does not establish that `SPEC.md` is absent or that code matches a ledger. Use Codex Desktop, Claude's Code tab, or a capable Cowork session for repository work.

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
| [Help](skills/help/SKILL.md) · `$craft:help` | Explain the workflow and discover current installed skills. | Nothing; bundled-resource reads only. |
| [Spec](skills/spec/SKILL.md) · `$craft:spec` | Define a change, capture current behavior, or amend intended behavior. | The meaning and content of repository-root `SPEC.md`. |
| [Build](skills/build/SKILL.md) · `$craft:build --next` | Implement and verify specified work. Also accepts `--all` or explicit task scope. | Implementation, tests, task statuses, staging, and scoped commits. |
| [Check](skills/check/SKILL.md) · `$craft:check` | Find disagreements between the current specification and code, or missing evidence. | Nothing; read-only. |
| [Audit](skills/audit/SKILL.md) · `$craft:audit` | Review whether decisions in an artifact are justified. A ledger is optional. | Nothing; read-only. |
| [Backprop](skills/backprop/SKILL.md) · `$craft:backprop` | Trace a confirmed defect and propose what the project needs to learn. | After confirmation, coordinates Spec and Build through a verified fix and commit. |
| [Distill](skills/distill/SKILL.md) · `$craft:distill` | Reduce a ledger to current intent and open work when obsolete or duplicate material accumulates. | Replaces `SPEC.md` only after an evidence-backed preview and explicit confirmation. |

`$craft:destill` is a [compatibility alias](skills/destill/SKILL.md) for `$craft:distill`. Neither spelling accepts arguments.

### 🧩 Supporting skills

| Skill / command | Use it for | Changes |
| --- | --- | --- |
| [Ponytail](skills/ponytail/SKILL.md) · `$craft:ponytail` | Choose the smallest correct solution. Select `lite`, `full`, or `ultra`; the default is `full`. | Guidance for the current work; does not authorize a new phase. |
| [Caveman](skills/caveman/SKILL.md) · `$craft:caveman` | Write compact specifications while retaining facts and conditions. | Wording and encoding within the current phase's authorized scope. |
| [Clarify](skills/clarify/SKILL.md) · `$craft:clarify` | Explain technical prose while preserving exact meaning and literals. | The requested prose; does not change requirements or phase authority. |

The startup hook loads Ponytail and Clarify guidance automatically. Skill entry loads whichever guidance is missing when hooks do not run. Build, Backprop, and Spec also activate Ponytail when they run. `stop ponytail` or `normal mode` suspends its guidance until the next activation; policy reload and Help preserve the mode and suspension. Clarify stays automatically available; the other skills require explicit invocation or their declared in-phase delegation.

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

Invoke the phase you want explicitly with either supported prefix or by selecting the installed skill. Review and specification work do not silently become implementation. Hooks load guidance, provide the legacy introduction, and validate zero-argument Distill/Destill commands, including Claude's native expansion payload. They never grant phase authority. Build resolves unrestricted request scopes within its own workflow.

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
skills/_shared/entry.md    Shared invocation, fallback, and capability contract
skills/help/introduction.md
                           Introductory prose shared by Help and the bare hook
hooks/session_start.py     Loads Ponytail and Clarify at session startup
hooks/spec_build_gate.py   Introduces Craft and validates Distill syntax
hooks/hooks.json           Claude default registration using executable + args
hooks/codex.json           Explicit Codex registration with Windows overrides
hooks/test_spec_build_gate.py
                           Regression checks for hooks and workflow contracts
.codex-plugin/plugin.json  Codex plugin manifest
.claude-plugin/            Claude manifest and shared marketplace catalog
plugin.yaml, __init__.py    Hermes Agent native plugin adapter
SPEC.md                   Craft's own specification and task ledger
FORMAT.md                 Local specification format
assets/                   README and desktop listing artwork
THIRD_PARTY_LICENSES/      Third-party notices
```

Run the existing regression suite from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hooks -p 'test_*.py' -v
claude plugin validate --strict .claude-plugin/marketplace.json
claude plugin validate --strict .claude-plugin/plugin.json
claude plugin validate --strict skills
hermes plugins doctor . --ci
git diff --check
```

The suite uses Python's standard library. It checks both command prefixes, native expansion payloads, metadata parity, dynamic Help inventory, policy failures, entry contracts, and configured launchers in paths containing spaces and Unicode. Unix and Windows Codex launcher tests run only on their native platform. On Windows, run `py -3 -m unittest discover -s hooks -p 'test_*.py' -v` with the documented interpreter prerequisites available.

The tests verify script output, registration counts, and selected instruction contracts. Actual desktop hook trust, loading once per event, and an agent following the instructions require the operator checks below. Claude's [direct execution form](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form) keeps plugin paths out of a shell; Codex's [Windows override](https://learn.chatgpt.com/docs/hooks) invokes `py -3` through PowerShell. Both registrations use the same Python scripts, UTF-8 resource reads, and five-second timeouts. Policy or router failures remain diagnostic and preserve usable guidance or the original prompt.

### 📦 Prepare an uploadable ZIP

After committing the source changes, run from the repository root:

```sh
mkdir -p output/releases
git archive --format=zip --output=output/releases/craft-0.2.5.zip HEAD
```

`git archive` packages committed files, including both manifests, the Hermes adapter, shared resources, Help, hook registrations, the beaver PNG, and `THIRD_PARTY_LICENSES/ponytail.txt`. Untracked artwork and `.git` are excluded. Check the archive holds one `.claude-plugin/plugin.json` and both manifests plus `plugin.yaml` report `0.2.5` before using Claude's Upload plugin route. Do not substitute a ZIP of the working directory, which may include local files or omit hidden manifests.

### 🧪 Desktop smoke checks — operator follow-up

Use a disposable project with the installed version, and record the client version and result. These checks remain separate from automated source validation:

1. **Menus and command entry:** select Help in each desktop menu and check both command spellings. In a repository-capable session, select Spec and Build explicitly. Test zero-argument Distill and Destill, rejected extra arguments, and unrestricted Build scopes. Viewing a command example must not start that phase.
2. **Hook trust and duplicates:** review and trust the configured hooks. In each host's hook view or logs, confirm one Craft handler per event. Codex selects `hooks/codex.json`; Claude discovers `hooks/hooks.json` once. Unrelated Claude slash commands must proceed unchanged.
3. **Startup, resume, and compaction:** confirm complete Ponytail and Clarify guidance. Select `lite` or `ultra`, suspend with `stop ponytail`, then resume/compact; reload alone must preserve both choices. Help preserves suspension; Spec, Build, and Backprop reactivate the selected mode.
4. **Hookless Chat:** run `/craft:help` and select Help from the menu with hooks absent. Review a supplied artifact with Audit and clarify supplied prose. Requests needing inaccessible source must retain the evidence gap and direct repository work to a capable mode.
5. **Cowork access:** test with and without access to the intended repository and required commands. The unavailable case must stop repository operations and explain missing access; the available case may complete the authorized workflow.
6. **Artwork and launchers:** check the Codex listing logo and composer icon, all four starter prompts, and launchers under paths containing spaces and Unicode on each native OS. The Windows launcher must be exercised on Windows with PowerShell and `py -3`; a skipped test is not runtime verification.

For contributions, inspect the relevant skill, hook, and ledger rules together. Keep changes focused, add a regression when behavior changes, and keep manifests and discovery metadata consistent. Describe the affected behavior and your validation in the pull request.

Editing this checkout does not update an installed plugin. Refresh or reinstall it through your host and start a new session when testing installed behavior.

## 📜 License and attribution

Craft is maintained by Benjamin Fransson. This repository currently has no project-wide license file.

Craft's Ponytail policy is adapted from [Ponytail](https://github.com/DietrichGebert/ponytail), version 4.8.4, by DietrichGebert. Its MIT license and upstream commit are preserved in [the third-party notice](THIRD_PARTY_LICENSES/ponytail.txt); that notice applies to the attributed material.

[↑ Back to top](#top)

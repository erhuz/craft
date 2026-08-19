from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

import spec_build_gate


class CraftPromptRouterTest(unittest.TestCase):
    def test_exact_craft_prompt_lists_every_skill_then_hooks(self) -> None:
        root = Path(__file__).resolve().parents[1]
        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-catalog",
            "turn_id": "turn-catalog",
            "cwd": str(root),
        }

        output = spec_build_gate.handle({**event, "prompt": "  $craft\n"})
        context = output["hookSpecificOutput"]["additionalContext"]
        catalog = context.split("\n\n", 1)[1]

        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            self.assertIn(f"`$craft:{skill.parent.name}` — ", catalog)

        hooks = json.loads((root / "hooks" / "hooks.json").read_text())["hooks"]
        for event_name, groups in hooks.items():
            for group in groups:
                for hook in group["hooks"]:
                    handler = Path(hook["command"].rsplit("/", 1)[-1].strip('"')).name
                    self.assertIn(f"`{event_name}` → `{handler}`", catalog)

        self.assertLess(catalog.index("## Skills"), catalog.index("## Hooks"))

    def test_craft_catalog_requires_the_bare_invocation(self) -> None:
        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-catalog",
            "turn_id": "turn-catalog",
            "cwd": "/tmp",
        }
        prompts = (
            "$CRAFT",
            "$craft --help",
            "$craft:plan",
            "show $craft",
            "$craft\nanything",
            "$craft.",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                output = spec_build_gate.handle({**event, "prompt": prompt})
                self.assertNotIn("CRAFT DEFAULT ACTION", str(output))

    def test_only_first_token_canonical_pre_build_invocations_activate(self) -> None:
        """Activate the gate only for exact semantic-phase command grammar."""

        prompts = (
            ("plan", "$craft:plan", True),
            ("spec_args", "$craft:spec amend constraints", True),
            ("distill", "$craft:distill", True),
            ("destill_alias", "$craft:destill", True),
            ("destill_trailing_space", "$craft:destill ", True),
            ("multiline", "\n\t$craft:plan\nexplore order imports", True),
            ("quoted", '"$craft:plan"', False),
            ("quoted_alias", '"$craft:destill"', False),
            ("embedded", "prefix$craft:spec suffix", False),
            (
                "explanatory",
                "Use $craft:plan to research order imports.",
                False,
            ),
            ("negated", "Do not run $craft:spec amend constraints", False),
            ("punctuated", "$craft:plan.", False),
            ("case_changed", "$Craft:spec amend constraints", False),
        )

        with tempfile.TemporaryDirectory() as data_directory:
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                for index, (case, prompt, activates) in enumerate(prompts):
                    with self.subTest(case=case, prompt=prompt):
                        event = {
                            "hook_event_name": "UserPromptSubmit",
                            "session_id": f"session-pre-build-{index}",
                            "turn_id": f"turn-pre-build-{index}",
                            "cwd": data_directory,
                        }
                        output = spec_build_gate.handle(
                            {**event, "prompt": prompt}
                        )
                        state = spec_build_gate._state_path(event)

                        self.assertIsNotNone(state)
                        self.assertEqual(state.exists(), activates)
                        if activates:
                            self.assertIn("PRE-BUILD GATE ACTIVE", str(output))
                        else:
                            self.assertIsNone(output)

    def test_implement_plan_requires_an_explicit_craft_phase(self) -> None:
        """Keep natural-language implementation blocked after semantic work."""

        with tempfile.TemporaryDirectory() as data_directory:
            event = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": data_directory,
            }
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                plan = spec_build_gate.handle(
                    {**event, "prompt": "$craft:plan explore order imports"}
                )
                self.assertIn("$craft:plan is read-only", str(plan))

                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertEqual(blocked["decision"], "block")

                spec = spec_build_gate.handle(
                    {**event, "prompt": "$craft:spec amend V1"}
                )
                self.assertIn("$craft:spec may edit SPEC.md only", str(spec))

                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement the plan"}
                )
                self.assertEqual(blocked["decision"], "block")

                distill = spec_build_gate.handle(
                    {**event, "prompt": "$craft:distill"}
                )
                self.assertIn("confirmed preview", str(distill))

                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertEqual(blocked["decision"], "block")

                alias = spec_build_gate.handle(
                    {**event, "prompt": "$craft:destill"}
                )
                self.assertIn("$craft:destill", str(alias))

                spec_build_gate.handle({**event, "prompt": "$craft:build --next"})
                allowed = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertIsNone(allowed)

                spec_build_gate.handle(
                    {**event, "prompt": "$craft:spec amend V2"}
                )
                spec_build_gate.handle(
                    {**event, "prompt": "$craft:full-loop --next --loop"}
                )
                allowed = spec_build_gate.handle(
                    {**event, "prompt": "Implement the plan"}
                )
                self.assertIsNone(allowed)

    def test_invalid_command_shaped_distill_invocations_block(self) -> None:
        """Reject lossy-workflow scope errors before phase state can change."""

        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-invalid-distill-scope",
            "turn_id": "turn-invalid-distill-scope",
            "cwd": "/tmp",
        }
        prompts = (
            "$craft:distill --candidate",
            "$craft:distill --promote",
            "$craft:distill --candidate --promote",
            "$craft:destill section",
            "$craft:distill $craft:spec",
            "$craft:distill.",
            "$craft:distill --candidate foo",
            "$craft:distill --promote unknown",
        )

        with patch.dict(os.environ, {}, clear=True):
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    output = spec_build_gate.handle({**event, "prompt": prompt})
                    self.assertEqual(output["decision"], "block")
                    self.assertEqual(
                        output["reason"],
                        spec_build_gate.INVALID_DISTILL_SCOPE_REASON,
                    )

        with tempfile.TemporaryDirectory() as data_directory:
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                spec_build_gate.handle(
                    {**event, "prompt": "$craft:spec amend §C"}
                )
                spec_build_gate.handle(
                    {**event, "prompt": "$craft:distill"}
                )
                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertEqual(blocked["decision"], "block")

    def test_explicit_build_tail_and_canonical_full_loop_unlock(self) -> None:
        """Accept any exact Build tail while keeping phase activation explicit."""

        prompts = (
            ("$craft:build", True),
            ("$craft:build --all", True),
            ("$craft:build T2", True),
            ("$craft:build T1 T2", True),
            ("$craft:build --next --all", True),
            ("$craft:build pim portal-manager emil", True),
            ("$craft:build --unknown", True),
            ("$craft:build\nportal-manager\npim", True),
            ("$craft:full-loop", True),
            ("$craft:full-loop T2 T3 --loop --max 2", True),
            ('"$craft:build --next"', False),
            ("Use $craft:build --next to implement the next task.", False),
            ("Do not run $craft:full-loop --next --loop.", False),
            ("$craft:build.", False),
        )

        with tempfile.TemporaryDirectory() as data_directory:
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                for index, (prompt, authorized) in enumerate(prompts):
                    with self.subTest(prompt=prompt):
                        event = {
                            "hook_event_name": "UserPromptSubmit",
                            "session_id": f"session-{index}",
                            "turn_id": f"turn-{index}",
                            "cwd": data_directory,
                        }
                        spec_build_gate.handle(
                            {**event, "prompt": "$craft:spec amend V2"}
                        )
                        spec_build_gate.handle({**event, "prompt": prompt})
                        output = spec_build_gate.handle(
                            {**event, "prompt": "Implement plan"}
                        )

                        if authorized:
                            self.assertIsNone(output)
                        else:
                            self.assertEqual(output["decision"], "block")

    def test_invalid_full_loop_invocations_block(self) -> None:
        """Keep Full Loop's coordinator grammar strict without limiting Build."""

        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-invalid-full-loop",
            "turn_id": "turn-invalid-full-loop",
            "cwd": "/tmp",
        }
        prompts = (
            "$craft:full-loop --max 2",
            "$craft:full-loop T1 --all",
            "$craft:full-loop --unknown",
        )

        with patch.dict(os.environ, {}, clear=True):
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    output = spec_build_gate.handle({**event, "prompt": prompt})
                    self.assertEqual(output["decision"], "block")
                    self.assertEqual(
                        output["reason"],
                        spec_build_gate.INVALID_FULL_LOOP_SCOPE_REASON,
                    )

        with tempfile.TemporaryDirectory() as data_directory:
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                spec_build_gate.handle(
                    {**event, "prompt": "$craft:spec amend V8"}
                )
                spec_build_gate.handle(
                    {**event, "prompt": "$craft:full-loop T1 --all"}
                )
                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertEqual(blocked["decision"], "block")

    def test_phase_state_failures_block_only_stateful_prompts(self) -> None:
        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-state-failure",
            "turn_id": "turn-state-failure",
            "cwd": "/tmp",
        }

        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(
                spec_build_gate.handle({**event, "prompt": "Explain the plan"})
            )
            unavailable = spec_build_gate.handle(
                {**event, "prompt": "$craft:spec amend V3"}
            )
        self.assertEqual(unavailable["decision"], "block")

        with tempfile.TemporaryDirectory() as data_directory:
            invalid_root = Path(data_directory) / "plugin-data"
            invalid_root.touch()
            with patch.dict(os.environ, {"PLUGIN_DATA": str(invalid_root)}):
                invalid = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
            self.assertEqual(invalid["decision"], "block")

            failures = (
                ("stat", "Implement plan"),
                ("touch", "$craft:spec amend V3"),
                ("unlink", "$craft:build --next"),
            )
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                for operation, prompt in failures:
                    with self.subTest(operation=operation):
                        with patch.object(
                            Path,
                            operation,
                            side_effect=PermissionError("denied"),
                        ):
                            output = spec_build_gate.handle(
                                {**event, "prompt": prompt}
                            )
                        self.assertEqual(output["decision"], "block")
                        self.assertEqual(
                            output["reason"],
                            spec_build_gate.PHASE_STATE_FAILURE_REASON,
                        )

    def test_implementation_defaults_are_canonical_invocations(self) -> None:
        root = Path(__file__).resolve().parents[1]
        agent_defaults = []
        for name in ("build", "full-loop"):
            metadata = (
                root / "skills" / name / "agents" / "openai.yaml"
            ).read_text()
            raw = next(
                line.split(":", 1)[1].strip()
                for line in metadata.splitlines()
                if line.strip().startswith("default_prompt:")
            )
            agent_defaults.append(json.loads(raw))

        plugin_defaults = json.loads(
            (root / ".codex-plugin" / "plugin.json").read_text()
        )["interface"]["defaultPrompt"]
        implementation_defaults = [
            prompt
            for prompt in plugin_defaults
            if "$craft:build" in prompt or "$craft:full-loop" in prompt
        ]

        self.assertCountEqual(agent_defaults, implementation_defaults)
        for prompt in implementation_defaults:
            with self.subTest(prompt=prompt):
                self.assertIsNotNone(
                    spec_build_gate.IMPLEMENTATION_INVOCATION.fullmatch(prompt)
                )

    def test_pre_build_defaults_are_canonical_invocations(self) -> None:
        """Expose canonical semantic defaults while keeping the alias explicit."""

        root = Path(__file__).resolve().parents[1]
        agent_defaults = []
        for name in ("plan", "spec", "distill"):
            metadata = (
                root / "skills" / name / "agents" / "openai.yaml"
            ).read_text()
            raw = next(
                line.split(":", 1)[1].strip()
                for line in metadata.splitlines()
                if line.strip().startswith("default_prompt:")
            )
            agent_defaults.append(json.loads(raw))

        expected = ["$craft:plan", "$craft:spec", "$craft:distill"]
        self.assertEqual(agent_defaults, expected)

        plugin_defaults = json.loads(
            (root / ".codex-plugin" / "plugin.json").read_text()
        )["interface"]["defaultPrompt"]
        pre_build_defaults = [
            prompt
            for prompt in plugin_defaults
            if prompt in expected
        ]
        self.assertCountEqual(pre_build_defaults, expected)
        for prompt in pre_build_defaults:
            with self.subTest(prompt=prompt):
                self.assertTrue(
                    spec_build_gate.PRE_BUILD_INVOCATION.fullmatch(prompt)
                    or spec_build_gate.DISTILL_INVOCATION.fullmatch(prompt)
                )

    def test_destill_is_an_explicit_alias_to_the_canonical_contract(self) -> None:
        """Keep the misspelled selector as metadata-documented delegation."""

        root = Path(__file__).resolve().parents[1]
        canonical = (root / "skills" / "distill" / "SKILL.md").read_text()
        alias = (root / "skills" / "destill" / "SKILL.md").read_text()
        metadata = (
            root / "skills" / "destill" / "agents" / "openai.yaml"
        ).read_text()
        canonical_normalized = " ".join(canonical.split())
        alias_normalized = " ".join(alias.split())

        self.assertIn(
            "$craft:destill is the explicit compatibility alias",
            canonical_normalized,
        )
        self.assertIn("Skill metadata registers one name", alias_normalized)
        self.assertIn("Read all of `../distill/SKILL.md`", alias_normalized)
        self.assertIn('default_prompt: "$craft:destill"', metadata)
        self.assertIn("metadata has one name", metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)


class CraftSkillPolicyTest(unittest.TestCase):
    def test_build_accepts_unrestricted_explicit_scope_before_work(self) -> None:
        """Remove command-shape and worktree-ownership rejection."""

        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills" / "build" / "SKILL.md").read_text()
        interpret = " ".join(
            skill.partition("## Interpret request")[2]
            .partition("\n## ")[0]
            .split()
        )
        load = " ".join(skill.partition("## Load")[2].partition("\n## ")[0].split())
        select = " ".join(
            skill.partition("## Select")[2].partition("\n## ")[0].split()
        )

        self.assertIn(
            "Treat exact first token `$craft:build` as implementation "
            "authorization",
            interpret,
        )
        self.assertIn(
            "Do not apply an argument whitelist or reject multiple IDs, "
            "selectors, paths, ledgers, or unfamiliar flags solely because of "
            "command shape",
            interpret,
        )
        self.assertIn("one invocation may span multiple ledgers", interpret)
        self.assertNotIn("INVALID_SCOPE", skill)
        self.assertIn(
            "explicit `SPEC.md`, file, or directory targets",
            load,
        )
        self.assertIn("Normalize real paths, deduplicate ledgers", load)
        self.assertIn(
            "Explicit task IDs: accept one or more, preflight all of them",
            select,
        )
        self.assertIn("Preflight the full ledger/task mapping", select)
        self.assertIn("absent ID → return `TASK_NOT_FOUND` and stop", load)
        self.assertIn(
            "`x` → report the task as already complete, treat it as a per-task "
            "strict no-op, and continue preflighting other requested tasks",
            load,
        )
        self.assertIn(
            "resume `~` from the current worktree state without requiring "
            "ownership proof",
            select,
        )
        self.assertLess(load.index("TASK_NOT_FOUND"), load.index("Read local"))
        self.assertLess(
            load.index("already complete"), load.index("Read local")
        )

    def test_check_reconciles_current_truth_sections_only(self) -> None:
        """Exclude historical defects from current-truth drift classification."""

        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills" / "check" / "SKILL.md").read_text()
        load = " ".join(skill.partition("## Load")[2].partition("\n## ")[0].split())
        report = " ".join(
            skill.partition("## Report")[2].partition("\n## ")[0].split()
        )

        self.assertIn(
            "no argument or `--all`: check `§G`, `§C`, `§I`, `§V`, and `§T`",
            load,
        )
        for section in ("§G", "§C", "§I", "§V", "§T"):
            with self.subTest(section=section):
                self.assertIn(f"## Check `{section}`", skill)
        self.assertIn(
            "`§B`: return `INVALID_SCOPE`; historical defect rows are not "
            "current truth and never participate in drift",
            load,
        )
        self.assertIn(
            "If any selected item is `DRIFT`, `VIOLATE`, `MISSING`, `EXTRA`, "
            "`STALE`, `INCOMPLETE`, or `UNVERIFIABLE`, do not output the clean "
            "sentinel.",
            report,
        )
        self.assertIn(
            "or is legitimately expected open work, output only:", report
        )

    def test_distill_requires_a_stable_confirmed_current_truth_rewrite(self) -> None:
        """Keep identifiers permanent and preserve intent and data-loss guards.

        Distillation is the only phase that removes ledger rows, so it is also
        the only place identifier stability can be lost. Pin the single
        confirmed mode, the permanent-gap rule, and the absence of any staging
        ledger that a renumbering workflow would otherwise need.
        """

        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills" / "distill" / "SKILL.md").read_text()
        caveman = (root / "skills" / "caveman" / "SKILL.md").read_text()
        spec = (root / "skills" / "spec" / "SKILL.md").read_text()
        build = (root / "skills" / "build" / "SKILL.md").read_text()
        normalized = " ".join(skill.split())
        caveman_normalized = " ".join(caveman.split())
        spec_normalized = " ".join(spec.split())

        for contract in (
            "Accept only the exact command `$craft:distill` with no arguments",
            "If any task is `~`, name that in-flight task and stop",
            "choose `defect`, `changed intent`, or `unknown`",
            "`defect` and `unknown` keep the intended ledger rule",
            "When two ledger claims express mutually exclusive intent",
            "requires an explicit answer",
            "Keep every surviving `V`, `T`, and `B` identifier and every task "
            "citation exactly as they stand",
            "Removed identifiers leave permanent gaps and are never reallocated",
            "Write nothing on the preview turn",
            "If any material input differs, report the preview as stale",
            "name each unanswered choice and write nothing",
            "staged, unstaged, and untracked state as the preview baseline",
            "Replace `SPEC.md` atomically with the confirmed content in one write",
            "Create no staging, candidate, migration, or archive file",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, normalized)

        for removed in (
            "--candidate",
            "--promote",
            "NEW_SPEC.md",
            "DISTILL_MIGRATION.md",
            "SPEC_ID_REFERENCE",
            "Renumber surviving",
        ):
            with self.subTest(removed=removed):
                self.assertNotIn(removed, skill)
                self.assertNotIn(removed, build)

        self.assertIn("`No distillation needed.`", skill)
        self.assertIn(
            "never reuse or renumber an identifier", caveman_normalized
        )
        self.assertIn(
            "survivors keep the identifiers and citations they already carry",
            caveman_normalized,
        )
        self.assertIn(
            "never reuse or renumber an existing or deleted ID", spec_normalized
        )
        self.assertIn("no phase renumbers an identifier", spec_normalized)
        self.assertIn("## Bootstrap from code", spec)
        self.assertNotIn("## Distill from code", spec)

    def test_build_uses_domain_artifacts_and_goal_based_commits(self) -> None:
        """Keep ledger labels out of Build outputs without stalling a task.

        The ban is worth nothing if an accidental reference halts work, so pin
        both halves: the prohibition that prevents references, and the final
        sweep that rewrites a slipped one instead of blocking completion.
        """

        root = Path(__file__).resolve().parents[1]
        build = (root / "skills" / "build" / "SKILL.md").read_text()
        backprop = (root / "skills" / "backprop" / "SKILL.md").read_text()
        full_loop = (root / "skills" / "full-loop" / "SKILL.md").read_text()
        artifact = " ".join(
            build.partition("## Implementation artifact contract")[2]
            .partition("\n## ")[0]
            .split()
        )

        self.assertIn(
            "Actual SPEC identifiers may appear only inside `SPEC.md` and exact "
            "Craft command selectors",
            artifact,
        )
        self.assertIn(
            "every authored or materially changed non-generated function",
            artifact,
        )
        self.assertIn(
            "Write every code comment and docstring only in English",
            artifact,
        )
        self.assertIn("including test functions", artifact)
        self.assertIn("Avoid introducing a reference in the first place", build)
        for sweep in (
            "Before running final gates, sweep the task-owned diff for SPEC "
            "identifiers",
            "Rewrite each one into domain meaning in place, then run the gates "
            "on the corrected diff",
            "never a blocker and never a reason to stop or reopen the task",
            "A bare `V<n>` or `T<n>` token with no reference context is not a "
            "violation",
        ):
            with self.subTest(sweep=sweep):
                self.assertIn(sweep, artifact)
        self.assertNotIn("volatile", build)

        self.assertIn("Feature commit: `build: <goal>`", build)
        self.assertIn("`fix: <root cause>`", build)
        self.assertIn("commit: `fix: <root cause>`", backprop)
        self.assertIn("task goals, commit SHAs", full_loop)
        self.assertNotIn("Feature commit: `T<n>:", build)
        self.assertNotIn("commit: `backprop B<n>", backprop)

    def test_build_continues_through_dirty_same_path_content(self) -> None:
        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills" / "build" / "SKILL.md").read_text()
        baseline = skill.partition("## Git baseline")[2].partition("\n## ")[0]
        normalized = " ".join(baseline.split())
        self.assertIn(
            "Continue from current staged, unstaged, and untracked content "
            "without requiring task-ownership proof.",
            normalized,
        )
        self.assertIn(
            "preserve and include the path as it stands instead of blocking",
            normalized,
        )

    def test_build_and_full_loop_share_next_task_precedence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        cases = (
            (
                "resumable",
                "If any `~` tasks exist, resume the lowest-numbered one before "
                "any `.` task.",
            ),
            ("new_task", "Otherwise, select the lowest-numbered `.` task."),
            ("closed", "If no `.` or `~` task exists, strict no-op."),
        )

        for skill_name in ("build", "full-loop"):
            skill = (root / "skills" / skill_name / "SKILL.md").read_text()
            selection = skill.partition("## Select")[2].partition("\n## ")[0]
            normalized = " ".join(selection.split())
            positions = []
            for case, expected in cases:
                with self.subTest(skill=skill_name, case=case):
                    self.assertIn(expected, normalized)
                    positions.append(normalized.index(expected))
            self.assertEqual(positions, sorted(positions))

    def test_spec_raw_defects_preserve_explicit_phase_authority(self) -> None:
        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills" / "spec" / "SKILL.md").read_text()
        dispatch = skill.partition("## Dispatch")[2].partition("## Create")[0]
        normalized = " ".join(dispatch.split())

        self.assertIn(
            "Raw bug or failed verification supplied: recommend an explicit "
            "`$craft:backprop` invocation; do not invoke Backprop or Build",
            normalized,
        )
        self.assertNotIn("supplied: invoke `$craft:backprop`", normalized)

    def test_skill_sentinels_stay_within_the_allowed_vocabulary(self) -> None:
        """Keep machine tokens scarce so a reader needs no decoder ring.

        An underscored capital is the shape every control sentinel takes, so
        scanning for that shape catches one reintroduced anywhere in the skill
        contracts while leaving per-item report verdict labels alone.
        """

        root = Path(__file__).resolve().parents[1]
        allowed = {
            "SPEC_MISSING",
            "FORMAT_MISSING",
            "INVALID_SCOPE",
            "TASK_NOT_FOUND",
            "NO_OPEN_TASKS",
        }
        sentinel_shape = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")

        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=skill.parent.name):
                found = set(sentinel_shape.findall(skill.read_text()))
                self.assertEqual(found - allowed, set())

    def test_review_results_are_judged_rather_than_string_matched(self) -> None:
        """Stop a reworded clean review from failing the finalization gate.

        Both reviewers previously had to emit one byte-exact sentence, so any
        hedge or rewording stalled a finished task. Pin the judged wording on
        the coordinator side and on the side that finalizes the commit.
        """

        root = Path(__file__).resolve().parents[1]
        full_loop = (root / "skills" / "full-loop" / "SKILL.md").read_text()
        build = (root / "skills" / "build" / "SKILL.md").read_text()

        self.assertIn(
            "Pass only when both reviewers report nothing left to change",
            " ".join(full_loop.split()),
        )
        self.assertIn(
            "Judge each report on its content, not on matching a fixed string",
            " ".join(full_loop.split()),
        )
        self.assertIn(
            "Judge that report on its content rather than matching a fixed "
            "string",
            " ".join(build.split()),
        )
        self.assertNotIn("outputs exactly", full_loop)
        self.assertNotIn("exact clean", build)

    def test_explicit_only_skills_disable_implicit_invocation(self) -> None:
        root = Path(__file__).resolve().parents[1]
        explicit_only = [
            skill
            for skill in sorted((root / "skills").glob("*/SKILL.md"))
            if "explicitly invoked" in skill.read_text().split("---", 2)[1]
        ]

        self.assertTrue(explicit_only)
        for skill in explicit_only:
            with self.subTest(skill=skill.parent.name):
                metadata = skill.parent / "agents" / "openai.yaml"
                self.assertTrue(metadata.is_file())
                self.assertIn(
                    "policy:\n  allow_implicit_invocation: false",
                    metadata.read_text(),
                )


if __name__ == "__main__":
    unittest.main()

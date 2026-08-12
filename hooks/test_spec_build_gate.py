from __future__ import annotations

import json
import os
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

    def test_implement_plan_requires_an_explicit_craft_phase(self) -> None:
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

    def test_only_canonical_implementation_invocations_unlock(self) -> None:
        prompts = (
            ("$craft:build", True),
            ("$craft:build --all", True),
            ("$craft:build T2", True),
            ("$craft:full-loop", True),
            ("$craft:full-loop T2 T3 --loop --max 2", True),
            ('"$craft:build --next"', False),
            ("Use $craft:build --next to implement the next task.", False),
            ("Do not run $craft:full-loop --next --loop.", False),
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


class CraftSkillPolicyTest(unittest.TestCase):
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

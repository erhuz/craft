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


if __name__ == "__main__":
    unittest.main()

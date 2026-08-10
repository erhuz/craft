from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

import spec_build_gate


class SpecBuildGateTest(unittest.TestCase):
    def test_implement_plan_requires_an_explicit_craft_phase(self) -> None:
        with tempfile.TemporaryDirectory() as data_directory:
            event = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": data_directory,
            }
            with patch.dict(os.environ, {"PLUGIN_DATA": data_directory}):
                spec = spec_build_gate.handle(
                    {**event, "prompt": "$craft:spec amend V1"}
                )
                self.assertIn("SPEC-ONLY", str(spec))

                blocked = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertEqual(blocked["decision"], "block")

                spec_build_gate.handle({**event, "prompt": "$craft:build --next"})
                allowed = spec_build_gate.handle(
                    {**event, "prompt": "Implement plan"}
                )
                self.assertIsNone(allowed)


if __name__ == "__main__":
    unittest.main()

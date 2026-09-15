"""Focused checks for Craft's Hermes prompt and skill adapter."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))

import craft


class Context:
    def __init__(self):
        self.skills = {}
        self.hooks = {}

    def register_skill(self, name, path):
        self.skills[name] = path

    def register_hook(self, name, callback):
        self.hooks[name] = callback


class HermesAdapterTest(unittest.TestCase):
    def test_all_shared_skills_and_prompt_hook_are_registered(self):
        ctx = Context()
        craft.register(ctx)
        self.assertEqual(
            ctx.skills,
            {
                skill.parent.name: skill
                for skill in (ROOT / "skills").glob("*/SKILL.md")
            },
        )
        self.assertEqual(ctx.hooks, {"pre_llm_call": craft.route_prompt})

    def test_phase_route_requires_exact_first_token(self):
        routed = craft.route_prompt("$craft:build --next")
        self.assertIn("skill_view('craft:build')", routed["context"])
        for prompt in (
            "show $craft:build --next",
            "`$craft:build --next`",
            '"$craft:build --next"',
            "$CRAFT:build --next",
            "$craft:buildish --next",
        ):
            with self.subTest(prompt=prompt):
                self.assertIsNone(craft.route_prompt(prompt))

    def test_intro_and_invalid_distill_do_not_load_a_phase(self):
        intro = craft.route_prompt("  $craft\n")["context"]
        self.assertIn("Craft is a workflow plugin", intro)
        self.assertIn("Do not call tools or invoke a skill", intro)
        invalid = craft.route_prompt("$craft:distill --candidate")["context"]
        self.assertIn("INVALID_SCOPE", invalid)
        self.assertNotIn("skill_view('craft:distill')", invalid)
        valid = craft.route_prompt("$craft:destill")["context"]
        self.assertIn("skill_view('craft:destill')", valid)

    def test_first_turn_reuses_complete_startup_policies(self):
        startup = craft.render_startup(ROOT)["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(craft.route_prompt("hello", is_first_turn=True), {"context": startup})
        self.assertIsNone(craft.route_prompt("hello", is_first_turn=False))


if __name__ == "__main__":
    unittest.main()

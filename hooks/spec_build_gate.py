#!/usr/bin/env python3
"""Introduce Craft and reject malformed Craft command shapes."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


DISTILL_INVOCATION = re.compile(r"\A\s*\$craft:(?:distill|destill)\s*\Z")
DISTILL_COMMAND_SHAPE = re.compile(
    r"\A\s*\$craft:(?:distill|destill)(?=\s|[.!?,;:]|$)"
)
CRAFT_DEFAULT_PROMPT = "$craft"
INVALID_DISTILL_SCOPE_REASON = (
    "INVALID_SCOPE: use $craft:distill or $craft:destill with no arguments."
)


def _skill_summary(skill: Path) -> str:
    metadata = skill.parent / "agents" / "openai.yaml"
    if metadata.is_file():
        match = re.search(
            r'^\s*short_description:\s*(.+?)\s*$',
            metadata.read_text(),
            re.MULTILINE,
        )
        if match:
            raw = match.group(1)
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = raw.strip("'\"")
            if isinstance(value, str) and value:
                return value

    body = skill.read_text().split("---", 2)[-1]
    paragraph: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    return " ".join(paragraph) or "No summary provided"


def render_introduction(root: Path) -> str:
    """Explain the workflow and discover skills from the installed plugin."""

    lines = [
        "# 🦫 Craft",
        "",
        "**Specify clearly. Build minimally. Verify deliberately.**",
        "",
        "Craft is a workflow plugin for Codex, Claude Code, and Hermes Agent. It keeps intended "
        "behavior and remaining work in `SPEC.md`, so you know what to build, "
        "how to verify it, and what is finished.",
        "",
        "## 🚀 Workflow",
        "",
        "1. **Specify** — `$craft:spec` defines behavior and tasks in `SPEC.md`. "
        "Review the specification before building.",
        "2. **Build** — `$craft:build --next` implements one task, runs the "
        "required checks, and creates a scoped local commit when they pass. "
        "Repeat for the remaining tasks.",
        "3. **Check** — `$craft:check` compares the specification with the code "
        "and reports mismatches or missing evidence without changing files.",
        "",
        "Invoke each phase explicitly. Creating a specification does not start "
        "Build, and a local commit does not push or deploy your changes.",
        "",
        "To get started, send `$craft:spec` with a description of your change. "
        "For an existing `SPEC.md`, use `$craft:spec amend <section>` with "
        "the requested change.",
        "",
        "## 🧰 Skills",
        "",
    ]
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        name = skill.parent.name
        lines.append(f"- `$craft:{name}` — {_skill_summary(skill)}")

    return "\n".join(lines)


def handle(event: dict[str, Any]) -> dict[str, Any] | None:
    """Introduce the workflow and reject a malformed Craft command shape.

    Routing is this hook's whole job. Authorization comes from the explicit
    skill invocation itself, so no prompt phrase and no stored session state
    may grant or withhold it, and an unusable host environment must never cost
    the user their prompt.
    """

    if event.get("hook_event_name") != "UserPromptSubmit":
        return None

    prompt = event.get("prompt")
    if not isinstance(prompt, str):
        return None

    if prompt.strip() == CRAFT_DEFAULT_PROMPT:
        introduction = render_introduction(Path(__file__).resolve().parents[1])
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "CRAFT DEFAULT ACTION. Reply with the Markdown introduction below "
                    "verbatim and nothing else. Do not call tools or invoke a skill.\n\n"
                    f"{introduction}"
                ),
            }
        }

    if (
        DISTILL_COMMAND_SHAPE.search(prompt) is not None
        and DISTILL_INVOCATION.fullmatch(prompt) is None
    ):
        return {
            "decision": "block",
            "reason": INVALID_DISTILL_SCOPE_REASON,
        }

    return None


def main() -> int:
    try:
        output = handle(json.load(sys.stdin))
    except Exception as error:
        output = {
            "systemMessage": (
                f"Craft prompt router failed: {type(error).__name__}: {error}"
            )
        }
    if output is not None:
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

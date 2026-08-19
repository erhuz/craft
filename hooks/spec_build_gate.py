#!/usr/bin/env python3
"""Render Craft's catalog and reject malformed Craft command shapes."""

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
# ponytail: replace prompt routing when both hosts expose a structured action ID.
IMPLEMENTATION_INVOCATION = re.compile(
    r"\s*\$craft:(?:"
    r"build(?:\s+[\s\S]*)?"
    r"|full-loop"
    r"(?:\s+(?:--next|--all|T[1-9]\d*(?:\s+T[1-9]\d*)*))?"
    r"(?:\s+--loop(?:\s+--max\s+[1-9]\d*)?)?"
    r")\s*"
)
CRAFT_DEFAULT_PROMPT = "$craft"
INVALID_DISTILL_SCOPE_REASON = (
    "INVALID_SCOPE: use $craft:distill or $craft:destill with no arguments."
)
INVALID_FULL_LOOP_SCOPE_REASON = (
    "INVALID_SCOPE: use a canonical $craft:full-loop invocation."
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


def render_catalog(root: Path) -> str:
    lines = ["# Craft", "", "## Skills", ""]
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        name = skill.parent.name
        lines.append(f"- `$craft:{name}` — {_skill_summary(skill)}")

    lines.extend(["", "## Hooks", ""])
    config = json.loads((root / "hooks" / "hooks.json").read_text())
    for event, groups in config.get("hooks", {}).items():
        for group in groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                scripts = re.findall(r"([^/\" ]+\.py)", command)
                handler = scripts[-1] if scripts else command
                lines.append(f"- `{event}` → `{handler}`")
    return "\n".join(lines)


def _first_token(prompt: str) -> str:
    stripped = prompt.strip()
    return stripped.split(maxsplit=1)[0] if stripped else ""


def handle(event: dict[str, Any]) -> dict[str, Any] | None:
    """Render the catalog and reject a malformed Craft command shape.

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
        catalog = render_catalog(Path(__file__).resolve().parents[1])
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "CRAFT DEFAULT ACTION. Reply with the Markdown catalog below "
                    "verbatim and nothing else. Do not call tools or invoke a skill.\n\n"
                    f"{catalog}"
                ),
            }
        }

    if (
        _first_token(prompt) == "$craft:full-loop"
        and IMPLEMENTATION_INVOCATION.fullmatch(prompt) is None
    ):
        return {
            "decision": "block",
            "reason": INVALID_FULL_LOOP_SCOPE_REASON,
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

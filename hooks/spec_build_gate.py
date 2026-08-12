#!/usr/bin/env python3
"""Render Craft's catalog and require explicit Build after Plan or Spec."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PRE_BUILD_INVOCATION = re.compile(
    r"(?:^|\s)\$craft:(?:plan|spec)(?=\s|$)", re.IGNORECASE
)
IMPLEMENTATION_INVOCATION = re.compile(
    r"(?:^|\s)\$craft:(?:build|full-loop)(?=\s|$)", re.IGNORECASE
)
IMPLEMENT_PLAN_PROMPTS = {"implement plan", "implement the plan"}
CRAFT_DEFAULT_PROMPT = "$craft"


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


def _state_path(event: dict[str, Any]) -> Path | None:
    data_root = os.environ.get("PLUGIN_DATA") or os.environ.get("CLAUDE_PLUGIN_DATA")
    session_id = event.get("session_id")
    if not data_root or not isinstance(session_id, str) or not session_id:
        return None
    key = hashlib.sha256(session_id.encode()).hexdigest()
    return Path(data_root) / "spec-build-gate" / key


def _remove(path: Path | None) -> None:
    if path is not None:
        path.unlink(missing_ok=True)


def _normalized(prompt: str) -> str:
    return " ".join(prompt.casefold().strip().rstrip(".!?").split())


def handle(event: dict[str, Any]) -> dict[str, Any] | None:
    path = _state_path(event)
    if event.get("hook_event_name") == "SessionEnd":
        _remove(path)
        return None
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

    if PRE_BUILD_INVOCATION.search(prompt):
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "CRAFT PRE-BUILD GATE ACTIVE. $craft:plan is read-only; "
                    "$craft:spec may edit SPEC.md only. Neither authorizes or "
                    "continues into Build."
                ),
            }
        }

    if IMPLEMENTATION_INVOCATION.search(prompt):
        _remove(path)
        return None

    if (
        _normalized(prompt) in IMPLEMENT_PLAN_PROMPTS
        and path is not None
        and path.exists()
    ):
        return {
            "decision": "block",
            "reason": (
                "Craft Plan and Spec do not authorize implementation; 'Implement "
                "plan' is not Build approval. Invoke $craft:plan to continue "
                "discovery, $craft:spec to encode the accepted brief, or explicitly "
                "invoke $craft:build or $craft:full-loop to implement code."
            ),
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

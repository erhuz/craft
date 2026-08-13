#!/usr/bin/env python3
"""Render Craft's catalog and require explicit Build after semantic phases."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PRE_BUILD_INVOCATION = re.compile(r"\A\s*\$craft:(?:plan|spec)(?=\s|$)")
DISTILL_INVOCATION = re.compile(
    r"\A\s*\$craft:(?:distill(?:(?:\s+--(?:candidate|promote))?\s*)?|destill)\Z"
)
DISTILL_COMMAND_SHAPE = re.compile(
    r"\A\s*\$craft:(?:distill|destill)(?=\s|[.!?,;:]|$)"
)
# ponytail: replace prompt grammar when both hosts expose a structured action ID.
IMPLEMENTATION_INVOCATION = re.compile(
    r"\s*\$craft:(?:"
    r"build(?:\s+(?:--next|--all|T[1-9]\d*))?"
    r"|full-loop"
    r"(?:\s+(?:--next|--all|T[1-9]\d*(?:\s+T[1-9]\d*)*))?"
    r"(?:\s+--loop(?:\s+--max\s+[1-9]\d*)?)?"
    r")\s*"
)
IMPLEMENTATION_COMMANDS = {"$craft:build", "$craft:full-loop"}
IMPLEMENT_PLAN_PROMPTS = {"implement plan", "implement the plan"}
CRAFT_DEFAULT_PROMPT = "$craft"
INVALID_DISTILL_SCOPE_REASON = (
    "INVALID_SCOPE: use $craft:distill, $craft:distill --candidate, "
    "$craft:distill --promote, or $craft:destill."
)
INVALID_IMPLEMENTATION_SCOPE_REASON = (
    "INVALID_SCOPE: use a canonical $craft:build or $craft:full-loop invocation."
)
PHASE_STATE_FAILURE_REASON = (
    "Craft phase state is unavailable; Build authorization cannot be verified."
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


def _state_exists(path: Path) -> bool:
    try:
        path.stat()
    except FileNotFoundError:
        return False
    return True


def _normalized(prompt: str) -> str:
    return " ".join(prompt.casefold().strip().rstrip(".!?").split())


def _first_token(prompt: str) -> str:
    stripped = prompt.strip()
    return stripped.split(maxsplit=1)[0] if stripped else ""


def handle(event: dict[str, Any]) -> dict[str, Any] | None:
    """Route exact Craft phases so semantic work cannot imply Build approval."""

    if event.get("hook_event_name") == "SessionEnd":
        _remove(_state_path(event))
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

    implementation = IMPLEMENTATION_INVOCATION.fullmatch(prompt) is not None
    if _first_token(prompt) in IMPLEMENTATION_COMMANDS and not implementation:
        return {
            "decision": "block",
            "reason": INVALID_IMPLEMENTATION_SCOPE_REASON,
        }

    distill = DISTILL_INVOCATION.fullmatch(prompt) is not None
    if DISTILL_COMMAND_SHAPE.search(prompt) is not None and not distill:
        return {
            "decision": "block",
            "reason": INVALID_DISTILL_SCOPE_REASON,
        }

    pre_build = PRE_BUILD_INVOCATION.search(prompt) is not None or distill
    implement_plan = _normalized(prompt) in IMPLEMENT_PLAN_PROMPTS
    if not (pre_build or implementation or implement_plan):
        return None

    try:
        path = _state_path(event)
        if path is None:
            raise RuntimeError("phase-state path is unavailable")

        if pre_build:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
            return {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "CRAFT PRE-BUILD GATE ACTIVE. $craft:plan is read-only; "
                        "$craft:spec may edit SPEC.md only; $craft:distill and "
                        "$craft:destill may materialize candidate or confirmed "
                        "distill artifacts only after a confirmed preview. None "
                        "authorizes or continues into Build."
                    ),
                }
            }

        if implementation:
            _remove(path)
            return None

        if implement_plan and _state_exists(path):
            return {
                "decision": "block",
                "reason": (
                    "Craft Plan, Spec, and Distill do not authorize implementation; "
                    "'Implement plan' is not Build approval. Invoke $craft:plan to "
                    "continue discovery, $craft:spec to encode the accepted brief, "
                    "$craft:distill to continue compaction, or explicitly invoke "
                    "$craft:build or $craft:full-loop to implement code."
                ),
            }
    except Exception:
        return {
            "decision": "block",
            "reason": PHASE_STATE_FAILURE_REASON,
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

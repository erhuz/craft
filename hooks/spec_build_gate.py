#!/usr/bin/env python3
"""Require explicit Craft Build after a Plan or Spec turn."""

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
                f"Craft spec/build gate failed: {type(error).__name__}: {error}"
            )
        }
    if output is not None:
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

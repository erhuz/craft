#!/usr/bin/env python3
"""Inject Craft's bundled Ponytail policy as SessionStart context (Codex & Claude Code)."""

from __future__ import annotations

import json
from pathlib import Path


def skill_body(text: str) -> str:
    if not text.startswith("---"):
        return text.strip()
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("Ponytail SKILL.md has incomplete frontmatter")
    return parts[2].strip()


def main() -> int:
    try:
        root = Path(__file__).resolve().parents[1]
        body = skill_body((root / "skills/ponytail/SKILL.md").read_text())
        output = {
            "systemMessage": "CRAFT:PONYTAIL:FULL",
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"CRAFT PONYTAIL ACTIVE — level: full\n\n{body}",
            },
        }
    except Exception as error:
        output = {
            "systemMessage": f"Craft Ponytail hook failed: {type(error).__name__}: {error}"
        }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

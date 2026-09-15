#!/usr/bin/env python3
"""Load Craft's bundled writing and implementation policies on session start."""

from __future__ import annotations

import json
from pathlib import Path


def skill_body(text: str) -> str:
    """Strip metadata and reject missing guidance so empty policies cannot load."""

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) != 3:
            raise ValueError("SKILL.md has incomplete frontmatter")
        text = parts[2]
    if not text.strip():
        raise ValueError("SKILL.md has no policy body")
    return text.strip()


def main() -> int:
    """Retain usable policies and user mode choices even if another policy fails."""

    root = Path(__file__).resolve().parents[1]
    policies = (
        (
            "ponytail",
            "CRAFT PONYTAIL — default: full; retain any user-selected "
            "mode or suspension.",
        ),
        ("clarify", "CRAFT CLARIFY"),
    )
    messages = []
    contexts = []
    for name, header in policies:
        try:
            body = skill_body((root / "skills" / name / "SKILL.md").read_text())
        except Exception as error:
            messages.append(
                f"Craft {name.title()} hook failed: {type(error).__name__}: {error}"
            )
        else:
            messages.append(f"CRAFT:{name.upper()}")
            contexts.append(f"{header}\n\n{body}")
    output = {"systemMessage": "\n".join(messages)}
    if contexts:
        output["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": "\n\n".join(contexts),
        }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

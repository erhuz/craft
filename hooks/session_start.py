#!/usr/bin/env python3
"""Load Craft's bundled writing and implementation policies on session start."""

from __future__ import annotations

import json
import re
from pathlib import Path


# Claude Code moves larger hook context to a file and injects only a preview.
CONTEXT_LIMIT = 10000
BUNDLED_PATH = re.compile(r"`((?:\.\./)?[\w./-]+\.md)`")


def resolve_paths(body: str, skill_dir: Path) -> str:
    """Make bundled relative references readable from injected context."""

    def absolute(match: re.Match[str]) -> str:
        target = (skill_dir / match.group(1)).resolve()
        return f"`{target}`" if target.is_file() else match.group(0)

    return BUNDLED_PATH.sub(absolute, body)


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


def render_startup(root: Path) -> dict:
    """Retain usable policies and user mode choices even if another policy fails."""

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
        skill = root / "skills" / name / "SKILL.md"
        try:
            body = resolve_paths(
                skill_body(skill.read_text(encoding="utf-8")), skill.parent
            )
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
    return output


def main() -> int:
    """Serialize shared guidance so native hooks and Hermes use one policy loader."""

    root = Path(__file__).resolve().parents[1]
    output = render_startup(root)
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Expose Craft's shared skills and prompt routing to Hermes Agent."""

import re
from pathlib import Path

from .hooks.session_start import render_startup
from .hooks.spec_build_gate import (
    DISTILL_COMMAND_SHAPE,
    DISTILL_INVOCATION,
    INVALID_DISTILL_SCOPE_REASON,
    render_introduction,
)


ROOT = Path(__file__).resolve().parent
PHASE = re.compile(r"\A\s*\$craft:([a-z][a-z0-9-]*)(?=\s|$)")


def route_prompt(user_message: str, is_first_turn: bool = False, **kwargs):
    """Load the requested Craft skill without granting a phase from a mention."""

    del kwargs
    if not isinstance(user_message, str):
        return None

    contexts = []
    if is_first_turn:
        startup = render_startup(ROOT)
        policy = startup.get("hookSpecificOutput", {}).get("additionalContext")
        if policy:
            contexts.append(policy)

    if user_message.strip() == "$craft":
        contexts.append(
            "CRAFT DEFAULT ACTION. Reply with the Markdown introduction below "
            "verbatim and nothing else. Do not call tools or invoke a skill.\n\n"
            + render_introduction(ROOT)
        )
    elif (
        DISTILL_COMMAND_SHAPE.search(user_message) is not None
        and DISTILL_INVOCATION.fullmatch(user_message) is None
    ):
        contexts.append(
            "CRAFT INVALID SCOPE. Reply with exactly "
            f"`{INVALID_DISTILL_SCOPE_REASON}` and nothing else. "
            "Do not call tools or change files."
        )
    elif match := PHASE.match(user_message):
        name = match.group(1)
        if (ROOT / "skills" / name / "SKILL.md").is_file():
            contexts.append(
                f"Craft invocation: load skill_view('craft:{name}') before acting "
                "and follow it for this exact user request. For sibling Craft "
                "skills referenced as ../<name>/SKILL.md, load "
                "skill_view('craft:<name>') with that sibling's name."
            )

    return {"context": "\n\n".join(contexts)} if contexts else None


def register(ctx):
    """Register existing skill files and one host-specific prompt hook."""

    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        ctx.register_skill(skill.parent.name, skill)
    ctx.register_hook("pre_llm_call", route_prompt)

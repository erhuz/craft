# 🦫 Craft

**Specify clearly. Build minimally. Verify deliberately.**

Craft is a workflow plugin for Codex and Claude. It keeps intended behavior
and remaining work in `SPEC.md`, so you know what to build, how to verify it,
and what is finished.

## 🚀 Workflow

1. **Specify** — `$craft:spec` defines behavior and tasks in `SPEC.md`.
   Review the specification before building.
2. **Build** — `$craft:build --next` implements one task, runs the required
   checks, and creates a scoped local commit when they pass. Repeat for the
   remaining tasks.
3. **Check** — `$craft:check` compares the specification with the code and
   reports mismatches or missing evidence without changing files.

Invoke each phase explicitly. Creating a specification does not start Build,
and a local commit does not push or deploy your changes.

To get started, send `$craft:spec` with a description of your change. For an
existing `SPEC.md`, use `$craft:spec amend <section>` with the requested change.
Claude's `/craft:<skill>` commands and explicit desktop skill selection run
the same workflows.

Repository work requires file and command access in Codex Desktop, Claude's
Code tab, or a capable Cowork session. In Claude Chat, use `/craft:help`, writing
guidance, and Audit or Clarify with supplied artifacts. Missing source evidence
remains an evidence gap.

## 🧰 Skills

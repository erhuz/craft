---
name: help
disable-model-invocation: true
description: >
  Explain Craft's workflow and current installed skills. Invoke as $craft:help
  or /craft:help, or select Help in the desktop skill menu. Works without hooks,
  Python, Git, or repository access and never starts a workflow phase.
---

# Help

Before this workflow, read and apply `../_shared/entry.md`.

Read `introduction.md` beside this skill and present its introductory prose.
Do not duplicate or reconstruct that prose from a separate template.

Under its Skills heading, discover the installed skills from the plugin's
sibling `*/SKILL.md` files or the host's installed Craft skill catalog. Include
each current skill once in name order. Use its `agents/openai.yaml`
`short_description` when available; otherwise use the skill's opening body
paragraph. Include both `$craft:<name>` and `/craft:<name>` for each entry.
Do not list resource directories as skills or assume a fixed skill count.
If bundled metadata cannot be read, report the missing inventory evidence and
use only entries the host actually exposes.

Read bundled resources through the host's file/resource tools. Do not run
Python, shell commands, Git, or inspect a repository to generate this response.
If the user asks about availability, explain the access requirements in the
shared entry contract. Help never invokes Spec, Distill, Build, or another
workflow phase, and quoted commands in its response grant no authority.

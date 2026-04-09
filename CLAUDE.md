# CLAUDE.md

This file provides guidance to Claude Code when working with this project.

## Project: my-project

Stack: not detected
Framework: TAUSIK (FRamework AI)

## TAUSIK Commands

```bash
.tausik/tausik status                  # project overview
.tausik/tausik session start           # start session
.tausik/tausik task list               # list tasks
.tausik/tausik task start <slug>       # claim + activate task
.tausik/tausik task done <slug>        # complete task
```

Full CLI ref: `.claude/references/project-cli.md`

## Workflow
- NEVER start coding without a task. Use `task start` first.
- ALWAYS use `.tausik/tausik` to run CLI commands (ensures correct venv Python).
- Always respond in the user's language.

## External Skills
External skills are managed via `skills.json` and auto-synced during bootstrap.
See `.claude/references/skill-catalog.md` for the full catalog with trigger keywords.
**When a user's request matches a trigger keyword for a not-installed skill, proactively suggest installing it.**

<!-- DYNAMIC:START -->
## Current State
Session: none | Branch: main | Version: 1.0.0
Tasks: 4/4 done, 0 active, 0 blocked
<!-- DYNAMIC:END -->

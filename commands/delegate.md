---
description: Delegate task to an AI coding agent CLI (Codex, Claude, OMP, Pi, Devin, etc.) via Orca CLI session or direct relay.
---

# /delegate Slash Command

Use this command to delegate tasks to background coding agent CLIs.

## Behavior

1. **Parse Agent, Model & Reasoning**:
   - Check if an agent name is specified in the prompt (e.g. `/delegate hey codex, build cars UI` or `/delegate @claude --model sonnet-3.7 --reasoning high refactor auth`).
   - Supports inline `--model <name>`, `--reasoning <effort>`, or `[model: <name>]`.
   - Runs in **YOLO mode by default** (auto-accepts all sandbox tool permissions without asking).
   - If **unspecified** (e.g. `/delegate build cars UI`):
     - Run `python3 skills/delegate/scripts/discover_agents.py`.
     - Ask the user which agent they would like to use among the detected agents.
     - Note: Task-to-model recommendations and complexity routing belong to our harness skill; user selects the agent for execution.

2. **Construct Self-Contained Brief**:
   - Create a structured brief with Objective, Scope Files, No-Commit rule, and Verification Gate.

3. **Dispatch via Orca CLI Session (or Direct CLI)**:
   - Prefer Orca CLI session (`ORCA terminal create` -> `send` -> `wait --for tui-idle` -> `read`).
   - Or run `python3 skills/delegate/scripts/delegate.py --agent <agent> --prompt "<prompt>" --json`.

4. **Review & Handback**:
   - Inspect `git status` and `git diff --stat`.
   - Run verification tests.
   - Present the changes to the user for review before any commit.

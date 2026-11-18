# Delegation Agent Guidelines

These rules apply whenever delegating tasks to external coding agent CLIs:

## 1. Review-First Safety Guardrail
- **NEVER** allow an implementer agent or delegation runner to execute `git commit`, `git push`, or alter git history.
- Always inspect `git status` and `git diff` after an implementer completes its turn.
- Present the uncommitted changes and verification results to the user for explicit approval before landing.

## 2. Self-Contained Briefs
- Implementer agents run in separate process sessions without access to the orchestrator's conversation history.
- Never delegate with vague references like "do what we discussed earlier" or "fix that bug".
- Always write an explicit brief containing:
  - Exact objective and acceptance criteria.
  - Target files to create or modify.
  - Hard constraint: "NO COMMITS".
  - Automated verification command (e.g. `npm test`, `pytest`).

## 3. Disambiguation when Agent is Unspecified
- If the user invokes `/delegate <task>` without naming an agent (e.g. `codex`, `claude`, `omp`, `pi`, `devin`):
  - Do not guess or silently pick an arbitrary agent.
  - Run agent discovery and prompt the user to choose an agent.
  - Clarify that task-to-model suitability evaluation is handled by the harness skill.

## 4. Prefer Orca Sessions in Orca Environments
- When working within Orca (`$TERM_PROGRAM == "Orca"` or Orca CLI available):
  - Prefer creating isolated worktrees and Orca interactive terminals.
  - Use `ORCA terminal wait --for tui-idle` for turn synchronization.

## 5. YOLO (Autonomous) Execution Default
- Delegated CLI sessions run with auto-approval and permissions pre-accepted by default (`--dangerously-skip-permissions`, `--yolo`, `--allow-all`).
- Background agents must not be blocked waiting on interactive user prompts for sandbox tool execution, file edits, or test commands.
- When model selection or reasoning effort is provided (`--model <name>`, `--reasoning <effort>`), pass the flags directly to the implementer CLI and inject reasoning directives into the task brief.

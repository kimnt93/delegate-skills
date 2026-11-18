---
name: codex-delegate
description: >-
  Delegate bounded implementation, refactoring, and feature tasks to the OpenAI Codex CLI (`codex`). Dispatches self-contained briefs, executes via Orca CLI session or direct headless execution, and returns git diffs for review before landing.
---

# Codex Delegate Skill

This skill delegates tasks specifically to the **OpenAI Codex CLI** (`codex`).

## When to Use
- Implementing UI components, standalone services, or bounded features with Codex.
- Offloading heavy refactorings or boilerplate generation to OpenAI Codex.
- You want the orchestrator or developer to review the diff and run tests before committing.

## How to Delegate to Codex

### 1. Formulate Brief
Create a self-contained brief emphasizing:
- Exact goal and files to modify.
- **NO COMMITS** rule.
- Verification command.

### 2. Dispatch
Execute via the bundled relay:
```bash
python3 skills/codex-delegate/scripts/relay.py --prompt "Create UI for cars display" --verify "npm test" --json
```

Or via universal `/delegate`:
```text
/delegate hey codex, create UI for cars display
```

### 3. Review Diff
Review touched files and `git diff` returned in the output before committing.

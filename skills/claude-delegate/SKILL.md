---
name: claude-delegate
description: >-
  Delegate bounded implementation, refactoring, and test writing to Anthropic Claude Code CLI (`claude`). Dispatches self-contained briefs via Orca session or direct headless execution, enforcing review-first diff verification before landing.
---

# Claude Code Delegate Skill

This skill delegates tasks specifically to **Claude Code** (`claude`).

## When to Use
- Deep codebase refactoring or complex cross-file feature development with Claude.
- Writing comprehensive unit or integration test suites.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Claude

```bash
python3 skills/claude-delegate/scripts/relay.py --prompt "Refactor user authentication service" --verify "npm test" --json
```

Or via `/delegate`:
```text
/delegate claude: refactor user authentication service
```

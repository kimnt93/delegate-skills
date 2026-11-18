---
name: commandcode-delegate
description: >-
  Delegate terminal coding tasks to Command Code CLI (`cmd` / `commandcode`). Dispatches briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# Command Code Delegate Skill

This skill delegates tasks specifically to **Command Code** (`cmd` / `commandcode`).

## How to Delegate to Command Code

```bash
python3 skills/commandcode-delegate/scripts/relay.py --prompt "Refactor user authentication routes" --json
```

Or via universal `/delegate`:
```text
/delegate command code: refactor user authentication routes
/delegate cmd: add database migrations
```

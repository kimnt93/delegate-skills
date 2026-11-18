---
name: cursor-delegate
description: >-
  Delegate implementation and editing tasks to the Cursor Agent CLI (`cursor-agent` / `cursor`). Dispatches self-contained briefs via Orca session or direct execution, enforcing review-first diff verification before landing.
---

# Cursor Agent Delegate Skill

This skill delegates tasks specifically to **Cursor Agent** (`cursor-agent` / `cursor`).

## How to Delegate to Cursor

```bash
python3 skills/cursor-delegate/scripts/relay.py --prompt "Add pagination and filter controls to table" --json
```

Or via `/delegate`:
```text
/delegate cursor: add pagination and filter controls to table
```

---
name: agy-delegate
description: >-
  Delegate coding tasks to Google Antigravity CLI (`agy`). Dispatches briefs via Orca session or direct headless execution, returning structured diff results.
---

# Google Antigravity (AGY) Delegate Skill

This skill delegates tasks specifically to **Antigravity CLI** (`agy`).

## How to Delegate to Antigravity

```bash
python3 skills/agy-delegate/scripts/relay.py --prompt "Generate API client types from OpenAPI spec" --json
```

Or via `/delegate`:
```text
/delegate agy: generate API client types from OpenAPI spec
```

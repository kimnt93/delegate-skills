---
name: pi-delegate
description: >-
  Delegate coding tasks to the Pi Coding Agent CLI (`pi`). Dispatches briefs via Orca session or direct headless execution, returning structured diff results.
---

# Pi Coding Agent Delegate Skill

This skill delegates tasks specifically to **Pi** (`pi`).

## How to Delegate to Pi

```bash
python3 skills/pi-delegate/scripts/relay.py --prompt "Add input validation to form fields" --json
```

Or via `/delegate`:
```text
/delegate hey pi, add input validation to form fields
```

---
name: opencode-delegate
description: >-
  Delegate coding tasks to OpenCode CLI (`opencode`). Dispatches briefs via Orca session or direct headless execution, returning structured diff results.
---

# OpenCode Delegate Skill

This skill delegates tasks specifically to **OpenCode** (`opencode`).

## How to Delegate to OpenCode

```bash
python3 skills/opencode-delegate/scripts/relay.py --prompt "Fix linting errors across codebase" --json
```

Or via `/delegate`:
```text
/delegate opencode: fix linting errors across codebase
```

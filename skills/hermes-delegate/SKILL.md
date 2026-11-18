---
name: hermes-delegate
description: >-
  Delegate autonomous coding, debugging, and tooling tasks to Hermes Agent CLI (`hermes-agent` / `hermes`). Dispatches briefs via Orca session or direct execution, returning structured diffs for review before landing.
---

# Hermes Agent Delegate Skill

This skill delegates tasks specifically to **Hermes Agent** (`hermes-agent` / `hermes`).

## When to Use
- Running autonomous coding, debugging, and system integration workflows with Hermes.
- Task execution leveraging Hermes Agent modules and tools.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Hermes

```bash
python3 skills/hermes-delegate/scripts/relay.py --prompt "Fix worker timeout and retry logic" --json
```

Or via universal `/delegate`:
```text
/delegate hermes: fix worker timeout and retry logic
/delegate hermes agent: implement rate limiting middleware
```

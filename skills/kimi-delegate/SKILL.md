---
name: kimi-delegate
description: >-
  Delegate long-context coding, translation, and implementation tasks to Moonshot Kimi Code CLI (`kimi`). Dispatches briefs via Orca session or direct execution, returning structured diffs for review before landing.
---

# Kimi Code Delegate Skill

This skill delegates tasks specifically to **Kimi Code** (`kimi`).

## When to Use
- Ultra-long context codebase analysis and multi-file code editing with Kimi.
- Multilingual documentation and code comments.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Kimi

```bash
python3 skills/kimi-delegate/scripts/relay.py --prompt "Analyze whole repo and add OpenAPI documentation" --json
```

Or via universal `/delegate`:
```text
/delegate kimi: analyze whole repo and add OpenAPI documentation
```

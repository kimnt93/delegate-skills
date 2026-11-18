---
name: grok-delegate
description: >-
  Delegate coding, deep reasoning, and repo-scale implementation tasks to xAI Grok Build CLI (`grok` / `xai`). Dispatches self-contained briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# xAI Grok Build Delegate Skill

This skill delegates tasks specifically to **xAI Grok Build** (`grok` / `xai`).

## When to Use
- Deep reasoning tasks, architectural roadmaps, and multi-file code editing using Grok.
- Offloading plan mode workflows or autonomous investigations.
- Automated CI/CD headless execution (`grok -p "$BRIEF"`).

## How to Delegate to Grok / xAI

```bash
python3 skills/grok-delegate/scripts/relay.py --prompt "Refactor caching layer to Redis cluster" --verify "pytest" --json
```

Or via universal `/delegate`:
```text
/delegate grok: refactor caching layer to Redis cluster
/delegate @xai optimize search ranking algorithms
```

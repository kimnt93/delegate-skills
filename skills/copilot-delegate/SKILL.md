---
name: copilot-delegate
description: >-
  Delegate bounded implementation and test writing tasks to GitHub Copilot CLI (`copilot` / `gh-copilot`). Dispatches briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# GitHub Copilot CLI Delegate Skill

This skill delegates tasks specifically to **GitHub Copilot CLI** (`copilot` / `gh copilot`).

## How to Delegate to Copilot

```bash
python3 skills/copilot-delegate/scripts/relay.py --prompt "Generate comprehensive test cases for order service" --verify "npm test" --json
```

Or via universal `/delegate`:
```text
/delegate copilot: generate comprehensive test cases for order service
/delegate github copilot: generate test cases
```

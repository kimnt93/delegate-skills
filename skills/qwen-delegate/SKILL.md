---
name: qwen-delegate
description: >-
  Delegate coding, refactoring, and multi-file implementation tasks to Alibaba Qwen Code CLI (`qwen` / `qwen-code`). Dispatches briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# Alibaba Qwen Code Delegate Skill

This skill delegates tasks specifically to **Qwen Code** (`qwen` / `qwen-code`).

## When to Use
- Code generation, bug repairs, and test writing optimized for Qwen 2.5 Coder models.
- Running inside Alibaba Qwen Code CLI terminal environments.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Qwen

```bash
python3 skills/qwen-delegate/scripts/relay.py --prompt "Implement quicksort and mergesort benchmarks" --verify "npm test" --json
```

Or via universal `/delegate`:
```text
/delegate qwen: implement quicksort and mergesort benchmarks
/delegate qwen code: fix unit test assertions
```

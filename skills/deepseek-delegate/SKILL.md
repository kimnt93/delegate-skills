---
name: deepseek-delegate
description: >-
  Delegate coding, algorithmic optimization, and reasoning tasks to DeepSeek Harness CLI (`dsh` / `deepseek`). Dispatches self-contained briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# DeepSeek Harness Delegate Skill

This skill delegates tasks specifically to **DeepSeek Harness** (`dsh` / `deepseek`).

## When to Use
- Algorithmic implementation, math-heavy reasoning, and code generation optimized for DeepSeek Coder / DeepSeek R1 models.
- Running inside local DeepSeek agent environments (`dsh`).
- Review-first workflows where changes are inspected before committing.

## How to Delegate to DeepSeek

```bash
python3 skills/deepseek-delegate/scripts/relay.py --prompt "Optimize tree traversal algorithm" --verify "pytest" --json
```

Or via universal `/delegate`:
```text
/delegate deepseek: optimize tree traversal algorithm
/delegate deepseek harness: refactor SQL query generator
```

---
name: muse-delegate
description: >-
  Delegate repository-scale refactoring, migrations, and multi-file engineering tasks to Meta Muse Code CLI (`muse` / `muse-code`). Dispatches briefs via Orca session or direct headless execution, returning structured diffs for review before landing.
---

# Meta Muse Code Delegate Skill

This skill delegates tasks specifically to **Meta Muse Code** (`muse` / `muse-code`).

## When to Use
- Large-scale refactoring, cross-package dependency migrations, and multi-agent code generation.
- Long-horizon engineering tasks powered by Muse Spark models.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Muse Code

```bash
python3 skills/muse-delegate/scripts/relay.py --prompt "Migrate API handlers to v2 router" --verify "make verify" --json
```

Or via universal `/delegate`:
```text
/delegate muse: migrate API handlers to v2 router
/delegate muse code: update serialization formats
```

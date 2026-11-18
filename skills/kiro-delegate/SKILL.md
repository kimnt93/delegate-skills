---
name: kiro-delegate
description: >-
  Delegate spec-driven software engineering and implementation tasks to Kiro CLI (`kiro-cli`). Dispatches self-contained briefs via Orca CLI session or direct headless execution, returning structured diffs for review before landing.
---

# Kiro CLI Delegate Skill

This skill delegates tasks specifically to **Kiro CLI** (`kiro-cli` / `kiro`).

## When to Use
- Spec-driven engineering tasks, architectural breakdowns, and multi-step implementations with Kiro.
- Tasks requiring structured planning and rigorous test-verified code changes.
- Review-first workflows where changes are inspected before committing.

## How to Delegate to Kiro

```bash
python3 skills/kiro-delegate/scripts/relay.py --prompt "Implement user onboarding wizard" --verify "npm test" --json
```

Or via universal `/delegate`:
```text
/delegate hey kiro, implement user onboarding wizard
```

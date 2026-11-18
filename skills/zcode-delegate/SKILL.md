---
name: zcode-delegate
description: >-
  Delegate low-level, binary, and algorithmic coding tasks to Z.AI ZCode CLI (`zcode`). Dispatches briefs via Orca session or direct execution, returning structured diffs for review before landing.
---

# Z.AI ZCode Delegate Skill

This skill delegates tasks specifically to **ZCode** (`zcode`).

## How to Delegate to ZCode

```bash
python3 skills/zcode-delegate/scripts/relay.py --prompt "Implement SIMD-accelerated string parser" --verify "cargo test" --json
```

Or via universal `/delegate`:
```text
/delegate zcode: implement SIMD-accelerated string parser
```

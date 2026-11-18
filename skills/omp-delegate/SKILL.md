---
name: omp-delegate
description: >-
  Delegate coding tasks to Oh My Pi CLI (`omp`). Dispatches self-contained briefs via Orca session or direct headless execution, returning structured diff results.
---

# Oh My Pi (OMP) Delegate Skill

This skill delegates tasks specifically to **Oh My Pi** (`omp`).

## How to Delegate to OMP

```bash
python3 skills/omp-delegate/scripts/relay.py --prompt "Implement table pagination" --json
```

Or via `/delegate`:
```text
/delegate @omp implement table pagination
```

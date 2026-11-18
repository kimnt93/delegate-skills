# Task Brief Templates

Use these templates when formulating self-contained briefs for delegated CLI agents.

---

## 1. UI Feature Implementation (e.g. Car Display)

```markdown
# TASK BRIEF: Car Display UI Component

## Objective
Implement a responsive Car Display UI component with a modern card grid layout, including image preview, car details (make, model, year, price, mileage), and filter badges.

## Target Scope Files
- Create: `src/components/CarCard.tsx`
- Create: `src/components/CarGrid.tsx`
- Create: `src/components/CarDisplay.test.tsx`
- Modify: `src/App.tsx` (wire up the new view)

## Reference Files for Conventions
- `src/components/CardBase.tsx`
- `src/theme/tokens.ts`

## Guardrails & Boundaries
- **NO COMMITS**: Do NOT run git commit or git push. Leave changes in the worktree.
- Restrict modifications strictly to the files listed above.
- Use Tailwind / existing CSS classes matching the project styling.
- All components must be strictly typed with TypeScript.

## Verification Gate
Run and ensure this command passes:
`npm test`
```

---

## 2. Bug Fix

```markdown
# TASK BRIEF: Fix Race Condition in Cache Invalidation

## Objective
Fix intermittent race condition where cache entries are read after invalidation has triggered but before backend socket confirms eviction.

## Target Scope Files
- Modify: `src/services/cacheManager.ts`
- Modify: `tests/cacheManager.test.ts`

## Boundaries & Constraints
- **NO COMMITS**: Keep changes uncommitted.
- Do not alter public method signatures of `CacheManager`.
- Add a concurrency regression test in `tests/cacheManager.test.ts`.

## Verification Gate
`pytest tests/cacheManager.test.ts`
```

---

## 3. Refactoring / Optimization

```markdown
# TASK BRIEF: Optimize Database Query Latency for User Feed

## Objective
Refactor the user feed aggregation query from sequential N+1 ORM fetches into a single batch query with proper indices.

## Target Scope Files
- Modify: `src/repositories/feedRepository.ts`
- Modify: `src/db/migrations/0042_add_feed_index.sql`

## Boundaries & Constraints
- **NO COMMITS**: Do not commit.
- Preserve the exact API output contract for `getFeedForUser`.

## Verification Gate
`make verify`
```

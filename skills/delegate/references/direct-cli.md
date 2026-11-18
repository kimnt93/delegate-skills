# Direct Headless CLI Relay Reference

When running outside an Orca desktop environment, tasks can be dispatched directly to implementer CLIs in non-interactive/headless mode.

---

## Agent CLI Matrix

| Agent | CLI Binary | Headless Execution Command | Notes |
| :--- | :--- | :--- | :--- |
| **OpenAI Codex** | `codex` | `codex exec "$BRIEF"` | Executes prompt non-interactively; writes code directly to workspace. |
| **Claude Code** | `claude` | `claude -p "$BRIEF"` | Runs in print/headless mode with specified prompt. |
| **Oh My Pi** | `omp` | `omp --prompt "$BRIEF"` | Executes prompt in headless automation mode. |
| **Pi Agent** | `pi` | `pi -p "$BRIEF"` | Fast headless CLI agent for code edits and refactors. |
| **Antigravity** | `agy` | `agy -p "$BRIEF"` | Non-interactive execution mode for Antigravity tasks. |
| **OpenCode** | `opencode` | `opencode exec "$BRIEF"` | Executes command non-interactively in workspace. |
| **Devin CLI** | `devin` | `devin run "$BRIEF"` | Dispatches task to Devin background worker. |
| **Aider** | `aider` | `aider --message "$BRIEF" --no-git` | `--no-git` prevents Aider from committing automatically. |
| **Cursor Agent** | `cursor-agent`| `cursor-agent "$BRIEF"` | Cursor headless agent runner. |
| **Cline CLI** | `cline` | `cline -p "$BRIEF"` | Cline CLI headless execution. |

---

## Guardrails for Direct Headless Relays

1. **Working Tree Isolation**:
   If possible, create a temporary git branch before headless execution:
   ```bash
   git checkout -b delegate-tmp-<agent>-<task>
   ```
2. **Review-First Enforcement**:
   - For tools with auto-commit flags (such as Aider), always pass `--no-git` or `--no-auto-commits`.
   - Never allow the runner to invoke `git push` or `git commit`.
3. **Execution Timeouts**:
   Always wrap direct execution with timeouts (default 300 seconds) to prevent infinite loops when an agent waits on interactive user input.

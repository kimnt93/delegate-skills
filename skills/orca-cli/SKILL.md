---
name: orca-cli
description: >-
  Operate Orca-managed worktrees, folder contexts, terminals, repos, automations, worktree
  comments, and Orca's embedded browser through the `orca` CLI. Use when the user says
  "$orca-cli", "Orca worktree", "child worktree", "spawn codex/claude in a worktree",
  "read/wait/send Orca terminal", "handoff" / "handover" / "give this to another agent", or
  "Orca browser". Also use for opening, testing, screenshotting, or checking how a local or
  external web page renders while working in Orca, unless the user or project names another
  browser tool; plain HTTP or API calls (curl, fetch) do not need it. Prefer it over raw git
  worktree, ad hoc PTYs, or Computer Use when Orca state is involved. Use Computer Use only
  when a visible window needs GUI control that a CLI, filesystem, or API cannot do.
---

# Orca CLI

This skill provides full instructions for controlling the Orca Agent Development Environment (ADE) through the `orca` CLI.

## 1. Resolve the CLI Executable for this Session

Choose the executable once and reuse it for every later command:

- If the `ORCA_CLI_COMMAND` environment variable is set, use its value. Orca exports this
  for managed WSL sessions.
- Otherwise, in a dev checkout whose session exposes `ORCA_DEV_REPO_ROOT`, use `orca-dev`.
- Otherwise, on Linux outside an Orca-managed terminal, use `orca-ide`. Never run bare
  `orca` there — outside Orca's terminals it normally resolves to the
  GNOME Orca screen reader (`/usr/bin/orca`) and starts speech on the user's machine.
- Otherwise, use `orca`.

*(Below, `ORCA` refers to the executable resolved above)*.

If the selected executable cannot run, report its exact error and stop. Do not fall through
to another executable, which could silently target a different Orca build.

---

## 2. Load the Version-Matched Guide (If Available)

```bash
ORCA skills get orca-cli
```
Prefer `--json`. If `skills get` is not available, proceed with the authoritative commands below.

---

## 3. Core CLI Commands

### Worktree Management
- **List worktrees**:
  ```bash
  ORCA worktree list --json
  ```
- **Create worktree**:
  ```bash
  ORCA worktree create --repo id:<repoId> --name <branch_or_task_name> --json
  ```
- **Delete worktree**:
  ```bash
  ORCA worktree delete --worktree <worktreeId> --json
  ```

### Terminal Management
- **List active terminals**:
  ```bash
  ORCA terminal list --json
  ```
- **Spawn agent terminal**:
  ```bash
  ORCA terminal create --worktree active --command "<agent_command>" --json
  ```
- **Send keystrokes / text to terminal**:
  ```bash
  ORCA terminal send --worktree active --text "<prompt_or_brief>" --enter --json
  ```
- **Wait for terminal idle state**:
  ```bash
  ORCA terminal wait --for tui-idle --timeout-ms 300000 --json
  ```
- **Read scrollback buffer**:
  ```bash
  ORCA terminal read --worktree active --lines 200 --json
  ```

### Embedded Browser Controls
- **Open URL in Orca's internal browser tab**:
  ```bash
  ORCA open-url --url <target_url>
  ```
- **Take screenshot**:
  ```bash
  ORCA browser screenshot --url <target_url> --path <output_path.png>
  ```

### Health & Status
- **Check Orca status**:
  ```bash
  ORCA status --json
  ```
- **Launch Orca if closed**:
  ```bash
  ORCA open --json
  ```

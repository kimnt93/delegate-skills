# delegate-skills

Universal multi-agent delegation plugin and CLI framework for AI coding agents. Delegates tasks to standalone CLI agents (Codex, Claude, Grok, DeepSeek, Kiro, Hermes, etc.) via **Orca CLI sessions** or direct headless relays.

Features **review-first diff verification**, **model selection**, **reasoning controls**, and **YOLO mode enabled by default** (auto-accepts all sandbox tool permissions without asking).

---

## Quick Install

Install the latest release across all detected AI agent harnesses with one command:

```bash
curl -fsSL https://raw.githubusercontent.com/kimnt93/delegate-skills/main/install.sh | bash
```

Or install from a local checkout via `make`:

```bash
git clone https://github.com/kimnt93/delegate-skills.git
cd delegate-skills
make install
```

### Supported Harnesses

The installer automatically detects and configures:
- **Antigravity / Gemini CLI**: Plugin and skills linked to `~/.gemini/config/`
- **Claude Code**: Skills and `/delegate` command linked to `~/.claude/`
- **OpenAI Codex CLI**: Skills and delegate prompt linked to `~/.codex/`
- **Oh My Pi (omp)**: Skills linked to `~/.omp/`
- **Stably AI Orca**: Skills linked to `~/.config/orca/`
- **OpenCode, Kiro, Grok, Hermes, Cursor**: Skills linked to their respective user config directories
- **Global Terminal Binary**: Links `delegate` CLI executable into `~/.local/bin/delegate`

---

## Usage

### 1. Slash Command (`/delegate`)
Inside your AI agent harness (Antigravity, Claude Code, Codex, Orca):

```text
# Explicit agent:
/delegate hey codex, implement UI for cars display

# With model and reasoning selection:
/delegate claude --model claude-3-7-sonnet --reasoning high: refactor authentication

# DeepSeek Harness:
/delegate deepseek harness --model deepseek-r1: optimize query execution plan

# Unspecified agent (will scan installed CLIs and prompt you):
/delegate build a responsive navigation bar
```

### 2. Standalone Terminal CLI
Run delegation directly from any shell:

```bash
# Natural prompt parsing
delegate --prompt "hey codex --model o3-mini, build cars UI"

# With test verification gate
delegate --agent claude --prompt "fix cache race condition" --verify "npm test"

# Dry-run plan preview
delegate --prompt "grok: refactor database pooling" --dry-run
```

---

## Supported AI Agent CLIs

| Agent | Default CLI | Orca Support | Natural Aliases |
| :--- | :--- | :---: | :--- |
| **OpenAI Codex** | `codex exec` | ✅ | `codex` |
| **Claude Code** | `claude -p` | ✅ | `claude` |
| **xAI Grok** | `grok -p` | ✅ | `grok`, `xai`, `grok build` |
| **DeepSeek Harness**| `dsh exec` | ✅ | `dsh`, `deepseek`, `deepseek harness` |
| **Kiro CLI** | `kiro-cli -p` | ✅ | `kiro`, `kiro-cli` |
| **Meta Muse Code** | `muse exec` | ✅ | `muse`, `muse code` |
| **Hermes Agent** | `hermes-agent`| ✅ | `hermes`, `hermes agent` |
| **Command Code** | `cmd` | ✅ | `cmd`, `command code`, `commandcode` |
| **GitHub Copilot** | `copilot -p` | ✅ | `copilot`, `github copilot`, `gh copilot` |
| **Moonshot Kimi** | `kimi -p` | ✅ | `kimi` |
| **Z.AI ZCode** | `zcode` | ✅ | `zcode` |
| **Alibaba Qwen** | `qwen -p` | ✅ | `qwen`, `qwen code` |
| **Oh My Pi** | `omp --prompt`| ✅ | `omp` |
| **Pi Coding Agent**| `pi -p` | ✅ | `pi` |
| **Devin CLI** | `devin run` | ✅ | `devin` |
| **Google Antigravity**| `agy -p` | ✅ | `agy` |
| **OpenCode** | `opencode exec`| ✅ | `opencode` |
| **Cursor Agent** | `cursor-agent`| ✅ | `cursor` |
| **Aider** | `aider --message`| ✅ | `aider` |
| **Cline CLI** | `cline -p` | ✅ | `cline` |
| **Qoder CLI** | `qoder` | ✅ | `qoder` |

---

## Development

```bash
# Run unit tests
make test

# Build distribution tarball
make dist

# Install to specific harness
make install-antigravity
make install-claude
make install-codex
make install-all

# Uninstall
make uninstall
```

---

## CI/CD Pipeline

When commits are pushed to `main`, `.github/workflows/release.yml` automatically:
1. Runs the test suite.
2. Builds the release tarball (`dist/delegate-skills.tar.gz`).
3. Creates a tagged GitHub Release with the release tarball and `install.sh`.

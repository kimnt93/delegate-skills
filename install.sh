#!/usr/bin/env bash
# ==============================================================================
# delegate-skills Installer
# Installs delegate-skills via GitHub Release across all detected AI agent harnesses
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kimnt93/delegate-skills/main/install.sh | bash
#   curl -fsSL ... | bash -s -- --version v1.0.0
#   ./install.sh [--harness all|antigravity|claude|codex|omp|orca] [--uninstall]
# ==============================================================================

set -e

REPO="kimnt93/delegate-skills"
GITHUB_URL="https://github.com/${REPO}"
RAW_URL="https://raw.githubusercontent.com/${REPO}/main"
INSTALL_BASE="${HOME}/.local/share/delegate-skills"
BIN_DIR="${HOME}/.local/bin"

VERSION="latest"
TARGET_HARNESS="auto"
DRY_RUN=false
UNINSTALL=false

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}==>${NC} ${BOLD}$1${NC}"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}Warning:${NC} $1"; }
log_error() { echo -e "${RED}Error:${NC} $1" >&2; }

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --version|-v)
      VERSION="$2"
      shift 2
      ;;
    --harness|-h)
      TARGET_HARNESS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --uninstall)
      UNINSTALL=true
      shift
      ;;
    --help)
      echo "delegate-skills installer"
      echo "Usage: install.sh [options]"
      echo "  --version <tag>    Install specific release version (default: latest)"
      echo "  --harness <name>   Target specific harness: auto, all, antigravity, claude, codex, omp, orca"
      echo "  --dry-run          Preview install steps without changing files"
      echo "  --uninstall        Remove installed skills, binaries, and harness links"
      exit 0
      ;;
    *)
      log_warn "Unknown argument: $1"
      shift
      ;;
  esac
done

# ------------------------------------------------------------------------------
# Check for local directory vs remote release download
# ------------------------------------------------------------------------------
SOURCE_DIR=""
CURRENT_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"

if [ -f "${CURRENT_SCRIPT_DIR}/plugin.json" ] && [ -d "${CURRENT_SCRIPT_DIR}/skills" ]; then
  SOURCE_DIR="${CURRENT_SCRIPT_DIR}"
  log_info "Installing from local source: ${SOURCE_DIR}"
else
  SOURCE_DIR="${INSTALL_BASE}"
fi

# ------------------------------------------------------------------------------
# Uninstall Routine
# ------------------------------------------------------------------------------
if [ "$UNINSTALL" = true ]; then
  log_info "Uninstalling delegate-skills..."
  
  if [ "$DRY_RUN" = true ]; then
    log_info "[dry-run] Would remove binary link ${BIN_DIR}/delegate and all harness links"
    exit 0
  fi

  # Remove binary symlink
  if [ -L "${BIN_DIR}/delegate" ] || [ -f "${BIN_DIR}/delegate" ]; then
    rm -f "${BIN_DIR}/delegate"
    log_success "Removed ${BIN_DIR}/delegate"
  fi

  # Remove harness links
  HARNESS_DIRS=(
    "${HOME}/.gemini/config/plugins/delegate-skills"
    "${HOME}/.gemini/config/skills/delegate"
    "${HOME}/.gemini/config/skills/orca-cli"
    "${HOME}/.claude/skills/delegate"
    "${HOME}/.claude/commands/delegate.md"
    "${HOME}/.codex/skills/delegate"
    "${HOME}/.codex/prompts/delegate.md"
    "${HOME}/.omp/skills/delegate"
    "${HOME}/.config/orca/skills/delegate"
    "${HOME}/.config/opencode/skills/delegate"
    "${HOME}/.kiro/skills/delegate"
    "${HOME}/.grok/skills/delegate"
    "${HOME}/.hermes/skills/delegate"
  )

  for dir in "${HARNESS_DIRS[@]}"; do
    if [ -L "$dir" ] || [ -e "$dir" ]; then
      rm -rf "$dir"
      log_success "Removed $dir"
    fi
  done

  if [ -d "${INSTALL_BASE}" ]; then
    rm -rf "${INSTALL_BASE}"
    log_success "Removed ${INSTALL_BASE}"
  fi

  log_success "delegate-skills successfully uninstalled."
  exit 0
fi

# ------------------------------------------------------------------------------
# Download Release if remote install
# ------------------------------------------------------------------------------
if [ "$SOURCE_DIR" = "${INSTALL_BASE}" ]; then
  log_info "Fetching delegate-skills release (${VERSION})..."
  
  ARCHIVE_URL=""
  if [ "$VERSION" = "latest" ]; then
    ARCHIVE_URL="${GITHUB_URL}/releases/latest/download/delegate-skills.tar.gz"
  else
    ARCHIVE_URL="${GITHUB_URL}/releases/download/${VERSION}/delegate-skills.tar.gz"
  fi

  if [ "$DRY_RUN" = false ]; then
    mkdir -p "${INSTALL_BASE}"
    TMP_TAR="/tmp/delegate-skills-$$.tar.gz"
    
    log_info "Downloading ${ARCHIVE_URL}..."
    if curl -fsSL "${ARCHIVE_URL}" -o "${TMP_TAR}" 2>/dev/null; then
      tar -xzf "${TMP_TAR}" -C "${INSTALL_BASE}"
      rm -f "${TMP_TAR}"
      log_success "Downloaded and extracted release to ${INSTALL_BASE}"
    else
      log_warn "Release archive not available yet. Falling back to main branch archive..."
      curl -fsSL "${GITHUB_URL}/archive/refs/heads/main.tar.gz" -o "${TMP_TAR}"
      tar -xzf "${TMP_TAR}" --strip-components=1 -C "${INSTALL_BASE}"
      rm -f "${TMP_TAR}"
      log_success "Extracted source to ${INSTALL_BASE}"
    fi
  else
    log_info "[dry-run] Would download ${ARCHIVE_URL} and extract to ${INSTALL_BASE}"
  fi
fi

# ------------------------------------------------------------------------------
# Install Global CLI Binary
# ------------------------------------------------------------------------------
CLI_SRC="${SOURCE_DIR}/bin/delegate"

if [ -f "${CLI_SRC}" ]; then
  if [ "$DRY_RUN" = false ]; then
    mkdir -p "${BIN_DIR}"
    chmod +x "${CLI_SRC}"
    ln -sfn "${CLI_SRC}" "${BIN_DIR}/delegate"
    log_success "Linked CLI: ${BIN_DIR}/delegate -> ${CLI_SRC}"
  else
    log_info "[dry-run] Would link ${BIN_DIR}/delegate -> ${CLI_SRC}"
  fi
fi

# ------------------------------------------------------------------------------
# Helper for Installing Skill Symlinks
# ------------------------------------------------------------------------------
install_skill_symlinks() {
  local target_skills_dir="$1"
  local harness_name="$2"
  
  if [ ! -d "${SOURCE_DIR}/skills" ]; then
    return
  fi

  if [ "$DRY_RUN" = false ]; then
    mkdir -p "${target_skills_dir}"
    for skill_path in "${SOURCE_DIR}/skills/"*; do
      if [ -d "$skill_path" ]; then
        local skill_name="$(basename "$skill_path")"
        local dest="${target_skills_dir}/${skill_name}"
        ln -sfn "$skill_path" "$dest"
      fi
    done
    log_success "Installed skills into ${harness_name}: ${target_skills_dir}"
  else
    log_info "[dry-run] Would link skills into ${harness_name}: ${target_skills_dir}"
  fi
}

# 1. Antigravity / Gemini CLI
if [ "$TARGET_HARNESS" = "auto" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "antigravity" ]; then
  GEMINI_BASE="${HOME}/.gemini/config"
  if [ -d "${HOME}/.gemini" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "antigravity" ]; then
    log_info "Detected Antigravity / Gemini environment..."
    if [ "$DRY_RUN" = false ]; then
      mkdir -p "${GEMINI_BASE}/plugins"
      mkdir -p "${GEMINI_BASE}/skills"
      ln -sfn "${SOURCE_DIR}" "${GEMINI_BASE}/plugins/delegate-skills"
      install_skill_symlinks "${GEMINI_BASE}/skills" "Antigravity"
      log_success "Configured Antigravity plugin and skills."
    else
      log_info "[dry-run] Would link plugin to ${GEMINI_BASE}/plugins/delegate-skills"
      install_skill_symlinks "${GEMINI_BASE}/skills" "Antigravity"
    fi
  fi
fi

# 2. Claude Code
if [ "$TARGET_HARNESS" = "auto" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "claude" ]; then
  CLAUDE_BASE="${HOME}/.claude"
  if [ -d "${CLAUDE_BASE}" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "claude" ]; then
    log_info "Configuring Claude Code harness..."
    if [ "$DRY_RUN" = false ]; then
      mkdir -p "${CLAUDE_BASE}/skills"
      mkdir -p "${CLAUDE_BASE}/commands"
      install_skill_symlinks "${CLAUDE_BASE}/skills" "Claude Code"
      if [ -f "${SOURCE_DIR}/commands/delegate.md" ]; then
        ln -sfn "${SOURCE_DIR}/commands/delegate.md" "${CLAUDE_BASE}/commands/delegate.md"
        log_success "Installed /delegate command into Claude Code: ${CLAUDE_BASE}/commands/delegate.md"
      fi
    else
      install_skill_symlinks "${CLAUDE_BASE}/skills" "Claude Code"
      log_info "[dry-run] Would link /delegate command to ${CLAUDE_BASE}/commands/delegate.md"
    fi
  fi
fi

# 3. OpenAI Codex CLI
if [ "$TARGET_HARNESS" = "auto" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "codex" ]; then
  CODEX_BASE="${HOME}/.codex"
  if [ -d "${CODEX_BASE}" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "codex" ]; then
    log_info "Configuring OpenAI Codex harness..."
    if [ "$DRY_RUN" = false ]; then
      mkdir -p "${CODEX_BASE}/skills"
      mkdir -p "${CODEX_BASE}/prompts"
      install_skill_symlinks "${CODEX_BASE}/skills" "Codex"
      if [ -f "${SOURCE_DIR}/commands/delegate.md" ]; then
        ln -sfn "${SOURCE_DIR}/commands/delegate.md" "${CODEX_BASE}/prompts/delegate.md"
        log_success "Installed delegate prompt into Codex: ${CODEX_BASE}/prompts/delegate.md"
      fi
    else
      install_skill_symlinks "${CODEX_BASE}/skills" "Codex"
      log_info "[dry-run] Would link delegate prompt to ${CODEX_BASE}/prompts/delegate.md"
    fi
  fi
fi

# 4. Oh My Pi (omp)
if [ "$TARGET_HARNESS" = "auto" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "omp" ]; then
  OMP_BASE="${HOME}/.omp"
  if [ -d "${OMP_BASE}" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "omp" ]; then
    log_info "Configuring Oh My Pi harness..."
    install_skill_symlinks "${OMP_BASE}/skills" "Oh My Pi"
  fi
fi

# 5. Stably AI Orca
if [ "$TARGET_HARNESS" = "auto" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "orca" ]; then
  ORCA_BASE="${HOME}/.config/orca"
  if [ -d "${ORCA_BASE}" ] || [ "$TERM_PROGRAM" = "Orca" ] || [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "orca" ]; then
    log_info "Configuring Stably AI Orca harness..."
    install_skill_symlinks "${ORCA_BASE}/skills" "Orca"
  fi
fi

# 6. Additional Harnesses (OpenCode, Kiro, Grok, Hermes, Cursor)
for h_spec in "opencode:${HOME}/.config/opencode" "kiro:${HOME}/.kiro" "grok:${HOME}/.grok" "hermes:${HOME}/.hermes" "cursor:${HOME}/.cursor"; do
  h_name="${h_spec%%:*}"
  h_dir="${h_spec##*:}"
  if [ "$TARGET_HARNESS" = "all" ] || [ "$TARGET_HARNESS" = "$h_name" ] || [ -d "$h_dir" ]; then
    install_skill_symlinks "${h_dir}/skills" "$h_name"
  fi
done

echo ""
log_success "${BOLD}delegate-skills installation complete!${NC}"
echo "Try running:"
echo "    delegate --prompt \"hey codex, build cars UI\" --dry-run"
echo "Or use /delegate inside your agent harness."

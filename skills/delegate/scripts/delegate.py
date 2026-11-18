#!/usr/bin/env python3
"""
delegate.py
Universal multi-agent delegation runner supporting Orca CLI sessions and direct headless CLI relays.
Supports:
  - Model selection (--model / -m)
  - Reasoning effort controls (--reasoning / -r)
  - Full YOLO mode (auto-approve / allow all tool permissions without asking, enabled by DEFAULT)
Outputs structured JSON conforming to delegate-relay.result.v1.
"""

import os
import sys
import re
import json
import time
import shutil
import argparse
import subprocess
from typing import Dict, List, Optional, Tuple

SCHEMA_VERSION = "delegate-relay.result.v1"

AGENT_CLI_MAPPINGS = {
    "codex": {
        "binary": "codex",
        "headless_args": ["exec"],
        "model_flag": "--model",
        "reasoning_flag": "--reasoning-effort",
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "codex"
    },
    "claude": {
        "binary": "claude",
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "claude"
    },
    "omp": {
        "binary": "omp",
        "headless_args": ["--prompt"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "omp"
    },
    "pi": {
        "binary": "pi",
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "pi"
    },
    "agy": {
        "binary": "agy",
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "agy"
    },
    "opencode": {
        "binary": "opencode",
        "headless_args": ["exec"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "opencode"
    },
    "devin": {
        "binary": "devin",
        "headless_args": ["run"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "devin"
    },
    "kiro": {
        "binary": "kiro-cli",
        "fallback_binaries": ["kiro"],
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "kiro-cli"
    },
    "grok": {
        "binary": "grok",
        "fallback_binaries": ["xai"],
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "grok"
    },
    "cursor": {
        "binary": "cursor-agent",
        "fallback_binaries": ["cursor"],
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "cursor-agent"
    },
    "deepseek": {
        "binary": "dsh",
        "fallback_binaries": ["deepseek"],
        "headless_args": ["exec"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "dsh"
    },
    "muse": {
        "binary": "muse",
        "fallback_binaries": ["muse-code"],
        "headless_args": ["exec"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--dangerously-skip-permissions"],
        "orca_cmd": "muse"
    },
    "hermes": {
        "binary": "hermes-agent",
        "fallback_binaries": ["hermes"],
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "hermes-agent"
    },
    "commandcode": {
        "binary": "cmd",
        "fallback_binaries": ["commandcode"],
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "cmd"
    },
    "copilot": {
        "binary": "copilot",
        "fallback_binaries": ["gh-copilot"],
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--allow-all"],
        "orca_cmd": "copilot"
    },
    "kimi": {
        "binary": "kimi",
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "kimi"
    },
    "zcode": {
        "binary": "zcode",
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "zcode"
    },
    "qwen": {
        "binary": "qwen",
        "fallback_binaries": ["qwen-code"],
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "qwen"
    },
    "aider": {
        "binary": "aider",
        "headless_args": ["--message", "--no-git"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yes-always"],
        "orca_cmd": "aider"
    },
    "cline": {
        "binary": "cline",
        "headless_args": ["-p"],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "cline"
    },
    "qoder": {
        "binary": "qoder",
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": "qoder"
    }
}

# Natural speech aliases
AGENT_ALIASES = {
    "xai": "grok",
    "grok build": "grok",
    "kiro cli": "kiro",
    "kiro-cli": "kiro",
    "deepseek harness": "deepseek",
    "dsh": "deepseek",
    "muse code": "muse",
    "muse-code": "muse",
    "hermes agent": "hermes",
    "hermes-agent": "hermes",
    "command code": "commandcode",
    "commandcode": "commandcode",
    "cmd": "commandcode",
    "github copilot": "copilot",
    "gh copilot": "copilot",
    "qwen code": "qwen",
    "qwen-code": "qwen",
    "cursor agent": "cursor",
    "cursor-agent": "cursor"
}

ADDITIONAL_SEARCH_DIRS = [
    os.path.expanduser("~/.local/bin"),
    os.path.expanduser("~/.grok/bin"),
    os.path.expanduser("~/.cargo/bin"),
    os.path.expanduser("~/.npm-global/bin"),
    "/usr/local/bin",
    "/usr/bin"
]

def find_binary(binary_name: str) -> Optional[str]:
    for directory in ADDITIONAL_SEARCH_DIRS:
        candidate = os.path.join(directory, binary_name)
        if os.path.lexists(candidate):
            return candidate
    return shutil.which(binary_name)

def resolve_orca_cli() -> Optional[str]:
    if os.environ.get("ORCA_CLI_COMMAND"):
        candidate = os.environ["ORCA_CLI_COMMAND"]
        if os.path.lexists(candidate):
            return candidate
    if os.environ.get("ORCA_DEV_REPO_ROOT"):
        hit = find_binary("orca-dev")
        if hit:
            return hit
    hit_ide = find_binary("orca-ide")
    if hit_ide:
        return hit_ide
    in_orca = bool(os.environ.get("TERM_PROGRAM") == "Orca" or os.environ.get("ORCA_AGENT_PANE"))
    if in_orca:
        hit_orca = find_binary("orca")
        if hit_orca:
            return hit_orca
    return hit_ide or find_binary("orca")

def normalize_agent_name(name: str) -> str:
    cleaned = name.lower().strip()
    return AGENT_ALIASES.get(cleaned, cleaned)

def parse_agent_from_prompt(raw_text: str) -> Tuple[Optional[str], Optional[str], Optional[str], str]:
    """
    Extracts (agent_id, model, reasoning, cleaned_task) from the prompt.
    Supports inline model and reasoning options:
      - /delegate hey codex --model o3-mini --reasoning high, build cars UI
      - /delegate claude (model: sonnet-3.7, reasoning: medium): refactor auth
      - /delegate @omp [model: claude-3-7-sonnet]: implement pagination
    """
    text = raw_text.strip()
    model = None
    reasoning = None

    # 1. Extract model (--model <m>, -m <m>, model: <m>, using model <m>)
    m_match = re.search(
        r'(?:--model|-m|model\s*[:=]|using\s+model\s+)\s*[\"\'\[]?([a-zA-Z0-9_\-\.:/]+)[\"\'\]]?',
        text,
        re.IGNORECASE
    )
    if m_match:
        model = m_match.group(1)
        text = text[:m_match.start()] + " " + text[m_match.end():]

    # 2. Extract reasoning (--reasoning <r>, -r <r>, reasoning: <r>, effort: <r>)
    r_match = re.search(
        r'(?:--reasoning|-r|reasoning\s*[:=]|effort\s*[:=])\s*[\"\'\[]?([a-zA-Z0-9_\-]+)[\"\'\]]?',
        text,
        re.IGNORECASE
    )
    if r_match:
        reasoning = r_match.group(1).lower()
        text = text[:r_match.start()] + " " + text[r_match.end():]

    # Clean leftover empty brackets or whitespace
    text = re.sub(r'[\(\[\{][\s,:;\-]*[\)\]\}]', '', text)
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 3. Match agent
    candidates = list(AGENT_ALIASES.keys()) + list(AGENT_CLI_MAPPINGS.keys())
    candidates = sorted(set(candidates), key=len, reverse=True)
    pattern = "|".join(re.escape(c) for c in candidates)

    m1 = re.match(
        rf"^(?:hey|hello|hi|please|delegate\s+to|ask|use)?\s*@?({pattern})[\s,:]+(.*)$",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if m1:
        raw_agent = m1.group(1).lower()
        task_body = re.sub(r'^[\s,:;\-\(\[\{\]]+', '', m1.group(2)).strip()
        return normalize_agent_name(raw_agent), model, reasoning, task_body

    m2 = re.match(rf"^@?({pattern})\s*[:\-]\s*(.*)$", text, re.IGNORECASE | re.DOTALL)
    if m2:
        raw_agent = m2.group(1).lower()
        task_body = re.sub(r'^[\s,:;\-\(\[\{\]]+', '', m2.group(2)).strip()
        return normalize_agent_name(raw_agent), model, reasoning, task_body

    clean_task = re.sub(r'^[\s,:;\-\(\[\{\]]+', '', text).strip()
    return None, model, reasoning, clean_task

def format_brief(task: str, scope_files: Optional[List[str]] = None,
                 verify_cmd: Optional[str] = None, model: Optional[str] = None,
                 reasoning: Optional[str] = None, yolo: bool = True) -> str:
    files_section = ""
    if scope_files:
        files_section = "\n## Target Scope Files\n" + "\n".join(f"- `{f}`" for f in scope_files)

    verify_section = ""
    if verify_cmd:
        verify_section = f"\n## Verification Gate\nRun and ensure this command exits 0:\n`{verify_cmd}`\n"

    model_section = ""
    if model or reasoning:
        parts = []
        if model:
            parts.append(f"- **Target Model**: `{model}`")
        if reasoning:
            parts.append(f"- **Reasoning Effort**: `{reasoning.upper()}` (Plan deeply before editing code)")
        model_section = "\n## Model & Reasoning Directives\n" + "\n".join(parts) + "\n"

    yolo_section = ""
    if yolo:
        yolo_section = """
## Execution Mode: YOLO (Autonomous / Zero Confirmation Prompts)
- **ALLOW ALL PERMISSIONS**: Never halt or ask for user confirmation. Execute file reads, edits, and terminal commands autonomously.
"""

    brief = f"""# TASK BRIEF

## Objective
{task}
{files_section}{model_section}{yolo_section}
## Guardrails & Boundaries
- **NO COMMITS**: Do NOT commit, push, or amend git history. Leave all changes in the working tree.
- Restrict modifications strictly to the objective.
- Ensure all newly introduced code adheres to existing project types, linting, and formatting.
{verify_section}
## Done Criteria
All required implementation is complete, compiles/passes syntax checks, and a brief summary of touched files is returned.
"""
    return brief.strip()

def run_git_diff_summary(cwd: str = ".") -> Tuple[List[str], str]:
    touched_files = []
    diff_stat = ""
    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if status_res.returncode == 0:
            for line in status_res.stdout.splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    touched_files.append(parts[1])

        diff_res = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if diff_res.returncode == 0:
            diff_stat = diff_res.stdout.strip()
    except Exception as e:
        diff_stat = f"(git inspection skipped: {e})"

    return touched_files, diff_stat

def run_verification(verify_cmd: str, cwd: str = ".") -> Tuple[bool, str]:
    try:
        res = subprocess.run(
            verify_cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=180
        )
        output = (res.stdout + "\n" + res.stderr).strip()
        return (res.returncode == 0), output
    except subprocess.TimeoutExpired:
        return False, "Verification timed out after 180 seconds."
    except Exception as e:
        return False, f"Verification failed with error: {e}"

def build_cli_invocation(agent: str, model: Optional[str] = None,
                         reasoning: Optional[str] = None, yolo: bool = True) -> Tuple[str, List[str]]:
    """Builds the binary command and parameter list with YOLO flags, model flags, and reasoning flags."""
    meta = AGENT_CLI_MAPPINGS.get(agent, {
        "binary": agent,
        "headless_args": [],
        "model_flag": "--model",
        "reasoning_flag": None,
        "yolo_flags": ["--yolo"],
        "orca_cmd": agent
    })

    args = list(meta.get("headless_args", []))

    # Add YOLO flags if enabled (default True)
    if yolo and meta.get("yolo_flags"):
        args.extend(meta["yolo_flags"])

    # Add model flag if specified
    if model and meta.get("model_flag"):
        args.extend([meta["model_flag"], model])

    # Add reasoning flag if supported
    if reasoning and meta.get("reasoning_flag"):
        args.extend([meta["reasoning_flag"], reasoning])

    return meta.get("orca_cmd", agent), args

def execute_orca_session(orca_bin: str, agent: str, brief: str,
                         timeout_ms: int, model: Optional[str] = None,
                         reasoning: Optional[str] = None, yolo: bool = True) -> Tuple[int, str]:
    orca_base, extra_args = build_cli_invocation(agent, model, reasoning, yolo)
    # Exclude headless runner flags from interactive Orca terminal spawn
    terminal_cmd_parts = [orca_base]
    if yolo and AGENT_CLI_MAPPINGS.get(agent, {}).get("yolo_flags"):
        terminal_cmd_parts.extend(AGENT_CLI_MAPPINGS[agent]["yolo_flags"])
    if model and AGENT_CLI_MAPPINGS.get(agent, {}).get("model_flag"):
        terminal_cmd_parts.extend([AGENT_CLI_MAPPINGS[agent]["model_flag"], model])
    if reasoning and AGENT_CLI_MAPPINGS.get(agent, {}).get("reasoning_flag"):
        terminal_cmd_parts.extend([AGENT_CLI_MAPPINGS[agent]["reasoning_flag"], reasoning])

    full_spawn_cmd = " ".join(terminal_cmd_parts)

    # 1. Create a terminal session with YOLO & model flags
    create_cmd = [orca_bin, "terminal", "create", "--worktree", "active", "--command", full_spawn_cmd, "--json"]
    proc = subprocess.run(create_cmd, capture_output=True, text=True)

    # 2. Send the brief
    send_cmd = [orca_bin, "terminal", "send", "--worktree", "active", "--text", brief, "--enter", "--json"]
    proc_send = subprocess.run(send_cmd, capture_output=True, text=True)
    if proc_send.returncode != 0:
        return proc_send.returncode, f"Failed to send prompt to Orca terminal: {proc_send.stderr}"

    # 3. Wait for tui-idle
    wait_cmd = [orca_bin, "terminal", "wait", "--for", "tui-idle", "--timeout-ms", str(timeout_ms), "--json"]
    proc_wait = subprocess.run(wait_cmd, capture_output=True, text=True)

    # 4. Read output buffer
    read_cmd = [orca_bin, "terminal", "read", "--worktree", "active", "--lines", "250", "--json"]
    proc_read = subprocess.run(read_cmd, capture_output=True, text=True)
    output_text = proc_read.stdout if proc_read.returncode == 0 else proc_wait.stdout

    return proc_wait.returncode, output_text

def execute_direct_cli(agent: str, brief: str, timeout_ms: int,
                       model: Optional[str] = None, reasoning: Optional[str] = None,
                       yolo: bool = True) -> Tuple[int, str]:
    meta = AGENT_CLI_MAPPINGS.get(agent)
    if not meta:
        return 1, f"Unknown agent: {agent}"

    candidates = [meta["binary"]] + meta.get("fallback_binaries", [])
    bin_path = None
    for b in candidates:
        hit = find_binary(b)
        if hit:
            bin_path = hit
            break

    if not bin_path:
        return 127, f"Agent binary for '{agent}' ({', '.join(candidates)}) not found in PATH or standard user directories."

    _, extra_args = build_cli_invocation(agent, model, reasoning, yolo)
    cmd = [bin_path] + extra_args + [brief]
    timeout_sec = max(10, timeout_ms // 1000)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        combined = (proc.stdout + "\n" + proc.stderr).strip()
        return proc.returncode, combined
    except subprocess.TimeoutExpired:
        return 124, f"Execution timed out after {timeout_sec} seconds."
    except Exception as e:
        return 1, f"Failed to execute CLI command: {e}"

def main():
    parser = argparse.ArgumentParser(description="Universal AI CLI Agent Delegation Runner")
    parser.add_argument("--agent", "-a", help="Target agent identifier")
    parser.add_argument("--model", "-m", help="Target model (e.g. o3-mini, claude-3-7-sonnet, deepseek-r1, gpt-4.5)")
    parser.add_argument("--reasoning", "-r", choices=["low", "medium", "high", "off", "min", "max"],
                        help="Reasoning effort level for models with extended thinking")
    parser.add_argument("--yolo", action="store_true", default=True,
                        help="YOLO mode: allow all tools/sandbox actions without interactive prompts (DEFAULT: True)")
    parser.add_argument("--no-yolo", "--safe", dest="yolo", action="store_false",
                        help="Disable YOLO mode (ask for permission before executing commands)")
    parser.add_argument("--prompt", "-p", help="Raw user prompt/task description")
    parser.add_argument("--brief", "-b", help="Path to markdown brief file")
    parser.add_argument("--mode", choices=["auto", "orca", "direct"], default="auto",
                        help="Execution mode: 'orca' (session-based), 'direct' (headless CLI), 'auto' (prefer orca if available)")
    parser.add_argument("--verify", "-v", help="Optional verification command to execute after implementation")
    parser.add_argument("--timeout-ms", type=int, default=300000, help="Execution timeout in milliseconds")
    parser.add_argument("--scope", nargs="*", help="List of file paths restricted for modifications")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without running")
    parser.add_argument("--json", action="store_true", help="Output machine-readable delegate-relay.result.v1 JSON")

    args = parser.parse_args()

    agent = args.agent
    model = args.model
    reasoning = args.reasoning
    raw_prompt = args.prompt or ""

    if args.brief and os.path.exists(args.brief):
        with open(args.brief, "r", encoding="utf-8") as f:
            brief_content = f.read()
    elif raw_prompt:
        detected_agent, detected_model, detected_reasoning, cleaned_task = parse_agent_from_prompt(raw_prompt)
        if not agent and detected_agent:
            agent = detected_agent
        if not model and detected_model:
            model = detected_model
        if not reasoning and detected_reasoning:
            reasoning = detected_reasoning
        brief_content = format_brief(cleaned_task or raw_prompt, args.scope, args.verify, model, reasoning, args.yolo)
    else:
        print("Error: Either --prompt or --brief must be specified.", file=sys.stderr)
        sys.exit(1)

    if not agent:
        print("Error: Target agent not specified and could not be detected from prompt.", file=sys.stderr)
        print("Please specify an agent via --agent <name> or e.g. '/delegate hey codex, <task>'", file=sys.stderr)
        sys.exit(2)

    agent = normalize_agent_name(agent)
    if agent not in AGENT_CLI_MAPPINGS:
        print(f"Warning: '{agent}' is not in standard known agents catalog. Proceeding with generic CLI call.", file=sys.stderr)

    orca_bin = resolve_orca_cli()
    use_orca = False

    if args.mode == "orca":
        if not orca_bin:
            print("Error: Orca mode requested but Orca CLI could not be resolved.", file=sys.stderr)
            sys.exit(1)
        use_orca = True
    elif args.mode == "auto":
        in_orca_env = bool(os.environ.get("TERM_PROGRAM") == "Orca" or os.environ.get("ORCA_AGENT_PANE"))
        if orca_bin and in_orca_env:
            use_orca = True
        else:
            use_orca = False
    else:
        use_orca = False

    if args.dry_run:
        plan = {
            "mode": "orca_session" if use_orca else "direct_cli",
            "agent": agent,
            "model": model,
            "reasoning": reasoning,
            "yolo_mode": args.yolo,
            "orca_binary": orca_bin if use_orca else None,
            "brief": brief_content,
            "verification_cmd": args.verify
        }
        if args.json:
            print(json.dumps(plan, indent=2))
        else:
            print("=== DELEGATION DRY-RUN PLAN ===")
            print(f"Agent: {agent}")
            print(f"Model: {model or '(default)'}")
            print(f"Reasoning Effort: {reasoning or '(default)'}")
            print(f"YOLO Mode: {'Enabled (Allow All Permissions)' if args.yolo else 'Disabled (Ask Permission)'}")
            print(f"Runner Mode: {'Orca Session' if use_orca else 'Direct Headless CLI'}")
            print("\n--- Brief Content ---")
            print(brief_content)
        return

    start_time = time.time()

    # Execute
    if use_orca:
        exit_code, output_text = execute_orca_session(orca_bin, agent, brief_content,
                                                      args.timeout_ms, model, reasoning, args.yolo)
        exec_mode = "orca_session"
    else:
        exit_code, output_text = execute_direct_cli(agent, brief_content, args.timeout_ms,
                                                    model, reasoning, args.yolo)
        exec_mode = "direct_cli"

    elapsed_ms = int((time.time() - start_time) * 1000)

    # Git inspections
    touched_files, diff_stat = run_git_diff_summary()

    # Verification gate
    verify_passed = None
    verify_output = None
    if args.verify:
        verify_passed, verify_output = run_verification(args.verify)

    status = "success" if exit_code == 0 else ("timeout" if exit_code == 124 else "error")

    result_payload = {
        "schema": SCHEMA_VERSION,
        "agent": agent,
        "model": model,
        "reasoning": reasoning,
        "yolo": args.yolo,
        "mode": exec_mode,
        "status": status,
        "exitCode": exit_code,
        "executionTimeMs": elapsed_ms,
        "touchedFiles": touched_files,
        "diffStat": diff_stat,
        "verification": {
            "command": args.verify,
            "passed": verify_passed,
            "output": verify_output
        } if args.verify else None,
        "summary": output_text[:1000] if output_text else "(No output recorded)"
    }

    if args.json:
        print(json.dumps(result_payload, indent=2))
    else:
        print(f"\n=== Delegation Result [{status.upper()}] ===")
        print(f"Agent: {agent} (model: {model or 'default'}, reasoning: {reasoning or 'default'})")
        print(f"YOLO Mode: {args.yolo}")
        print(f"Runner: {exec_mode} | Exit Code: {exit_code} ({elapsed_ms}ms)")
        if touched_files:
            print("\nTouched Files:")
            for f in touched_files:
                print(f"  • {f}")
        if diff_stat:
            print(f"\nDiff Stat:\n{diff_stat}")
        if args.verify:
            v_status = "PASSED" if verify_passed else "FAILED"
            print(f"\nVerification [{v_status}]: {args.verify}")
            if not verify_passed and verify_output:
                print(f"Verification Output:\n{verify_output[:500]}")
        print("\nReview-first guardrail: All changes are uncommitted. Review before committing.")

if __name__ == "__main__":
    main()

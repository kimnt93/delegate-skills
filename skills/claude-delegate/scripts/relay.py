#!/usr/bin/env python3
"""
relay.py for claude-delegate
Dispatches delegation briefs specifically to the Claude Code CLI.
"""

import sys
import os
import subprocess

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    delegate_script = os.path.join(root, "delegate/scripts/delegate.py")
    args = [sys.executable, delegate_script, "--agent", "claude"] + sys.argv[1:]
    res = subprocess.run(args)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()

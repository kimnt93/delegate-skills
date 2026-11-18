#!/usr/bin/env python3
"""
Unit tests for delegate-skills.
Tests agent parsing, model & reasoning selection, YOLO mode defaults, brief generation, and discovery routines.
"""

import os
import sys
import unittest

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills/delegate/scripts"))
sys.path.insert(0, scripts_dir)

from delegate import parse_agent_from_prompt, format_brief, build_cli_invocation
from discover_agents import discover_agents

class TestDelegateSkills(unittest.TestCase):

    def test_parse_agent_explicit_hey(self):
        prompt = "hey codex, i want to create UI for cars display"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "codex")
        self.assertIsNone(model)
        self.assertIsNone(reasoning)
        self.assertEqual(task, "i want to create UI for cars display")

    def test_parse_agent_with_model_and_reasoning(self):
        prompt = "hey codex --model o3-mini --reasoning high, build cars UI"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "codex")
        self.assertEqual(model, "o3-mini")
        self.assertEqual(reasoning, "high")
        self.assertEqual(task, "build cars UI")

    def test_parse_agent_with_bracket_syntax(self):
        prompt = "claude (model: claude-3-7-sonnet, reasoning: medium): refactor auth"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "claude")
        self.assertEqual(model, "claude-3-7-sonnet")
        self.assertEqual(reasoning, "medium")
        self.assertEqual(task, "refactor auth")

    def test_parse_agent_colon_syntax(self):
        prompt = "claude: refactor database connection pooling"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "claude")
        self.assertEqual(task, "refactor database connection pooling")

    def test_parse_agent_at_mention(self):
        prompt = "@omp implement pagination for table view"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "omp")
        self.assertEqual(task, "implement pagination for table view")

    def test_parse_agent_delegate_to(self):
        prompt = "delegate to pi: add form validation"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertEqual(agent, "pi")
        self.assertEqual(task, "add form validation")

    def test_parse_agent_unspecified(self):
        prompt = "i want to create UI for cars display"
        agent, model, reasoning, task = parse_agent_from_prompt(prompt)
        self.assertIsNone(agent)
        self.assertEqual(task, "i want to create UI for cars display")

    def test_parse_new_agents(self):
        cases = [
            ("hey kiro, build dashboard", "kiro", "build dashboard"),
            ("grok: optimize latency", "grok", "optimize latency"),
            ("@xai analyze metrics", "grok", "analyze metrics"),
            ("cursor: fix css styling", "cursor", "fix css styling"),
            ("deepseek harness: rewrite query planner", "deepseek", "rewrite query planner"),
            ("muse code: migrate react components", "muse", "migrate react components"),
            ("hermes agent: handle retry logic", "hermes", "handle retry logic"),
            ("command code: run benchmarks", "commandcode", "run benchmarks"),
            ("github copilot: generate tests", "copilot", "generate tests"),
            ("kimi: translate comments", "kimi", "translate comments"),
            ("zcode: decompile routine", "zcode", "decompile routine"),
            ("qwen code: solve competitive puzzle", "qwen", "solve competitive puzzle")
        ]
        for prompt, expected_agent, expected_task in cases:
            agent, model, reasoning, task = parse_agent_from_prompt(prompt)
            self.assertEqual(agent, expected_agent, f"Failed agent for: {prompt}")
            self.assertEqual(task, expected_task, f"Failed task for: {prompt}")

    def test_format_brief_with_model_and_yolo(self):
        task = "create UI for cars display"
        scope = ["src/components/CarDisplay.tsx"]
        verify = "npm test"
        brief = format_brief(task, scope, verify, model="o3-mini", reasoning="high", yolo=True)

        self.assertIn("# TASK BRIEF", brief)
        self.assertIn("create UI for cars display", brief)
        self.assertIn("Target Model", brief)
        self.assertIn("o3-mini", brief)
        self.assertIn("Reasoning Effort", brief)
        self.assertIn("HIGH", brief)
        self.assertIn("YOLO", brief)
        self.assertIn("ALLOW ALL PERMISSIONS", brief)
        self.assertIn("NO COMMITS", brief)
        self.assertIn("src/components/CarDisplay.tsx", brief)
        self.assertIn("npm test", brief)

    def test_build_cli_invocation_yolo_default(self):
        orca_cmd, extra_args = build_cli_invocation("codex", model="o3-mini", reasoning="high", yolo=True)
        self.assertEqual(orca_cmd, "codex")
        self.assertIn("--dangerously-skip-permissions", extra_args)
        self.assertIn("--model", extra_args)
        self.assertIn("o3-mini", extra_args)
        self.assertIn("--reasoning-effort", extra_args)
        self.assertIn("high", extra_args)

    def test_discover_agents(self):
        data = discover_agents()
        self.assertIn("orca", data)
        self.assertIn("detected_agents", data)
        self.assertIn("missing_agents", data)
        detected = data["detected_agents"]
        self.assertTrue("codex" in detected or "claude" in detected or "omp" in detected or "agy" in detected or "pi" in detected)

if __name__ == "__main__":
    unittest.main()

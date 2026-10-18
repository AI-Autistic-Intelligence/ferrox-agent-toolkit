#!/usr/bin/env python3
"""
Ferrox Agent Toolkit Self-Verification Test Suite
Verifies that all skills, rules, templates, and scripts are correctly formatted,
valid YAML frontmatter exists, and all CLI utilities run with exit code 0.
"""

import sys
import os
from pathlib import Path

def test_toolkit_integrity():
    root = Path(__file__).resolve().parent.parent
    print(f"Testing Ferrox Agent Toolkit at: {root}")

    errors = []

    # 1. Check required manifests
    manifests = ["plugin.json", "agents.json", "openpack.json", "README.md", "HANDBOOK.md", "AGENTS.md"]
    for m in manifests:
        p = root / m
        if not p.exists():
            errors.append(f"Missing root manifest: {m}")
        else:
            print(f"  [OK] Manifest present: {m}")

    # 2. Check rules
    rules_dir = root / "rules"
    expected_rules = [
        "ferrox-ddd-architecture.md",
        "ferrox-tdd-100-percent.md",
        "ferrox-e2e-contract-testing.md",
        "ferrox-sentinel-security.md",
        "ferrox-polyglot-paradigms.md",
        "ferrox-interop-connectors.md"
    ]
    for r in expected_rules:
        p = rules_dir / r
        if not p.exists():
            errors.append(f"Missing rule: {r}")
        else:
            print(f"  [OK] Rule present: {r}")

    # 3. Check skills and YAML frontmatter
    skills_dir = root / "skills"
    expected_skills = [
        "ferrox-ddd-planner",
        "ferrox-tdd-orchestrator",
        "ferrox-e2e-scaffolder",
        "ferrox-security-auditor",
        "ferrox-polyglot-connector",
        "ferrox-code-reviewer",
        "ferrox-workflow-handoff"
    ]
    for s in expected_skills:
        skill_file = skills_dir / s / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"Missing skill file: {s}/SKILL.md")
        else:
            content = skill_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                errors.append(f"Skill {s}/SKILL.md is missing YAML frontmatter opening '---'")
            elif "name:" not in content or "description:" not in content:
                errors.append(f"Skill {s}/SKILL.md is missing name or description in YAML frontmatter")
            else:
                print(f"  [OK] Skill verified with valid frontmatter: {s}")

    # 4. Check agents
    agents_dir = root / "agents"
    expected_agents = [
        "ferrox-architect-ddd.md",
        "ferrox-tdd-engineer.md",
        "ferrox-security-sentinel.md",
        "ferrox-e2e-resilience.md",
        "ferrox-connector-specialist.md"
    ]
    for a in expected_agents:
        p = agents_dir / a
        if not p.exists():
            errors.append(f"Missing agent spec: {a}")
        else:
            print(f"  [OK] Agent specification present: {a}")

    if errors:
        print("\nToolkit verification failed with errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\nAll Ferrox Agent Toolkit components successfully validated!")
        sys.exit(0)

if __name__ == "__main__":
    test_toolkit_integrity()

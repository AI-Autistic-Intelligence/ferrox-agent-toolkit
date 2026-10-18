#!/usr/bin/env python3
"""
Ferrox Agent Toolkit Self-Verification Test Suite (Dual-Layer Architecture)
Verifies:
1. JSON manifest syntax and structure (plugin.json, agents.json, openpack.json)
2. All 14 rules exist and are non-empty
3. All 13 skills exist with valid YAML frontmatter ('---', name, description)
4. All 7 specialized agent specifications exist and are non-empty
5. Key templates and scripts exist
"""

import sys
import os
import json
from pathlib import Path

def test_toolkit_integrity():
    root = Path(__file__).resolve().parent.parent
    print(f"🛡️  Verifying Ferrox Agent Toolkit at: {root}\n")

    errors = []

    # 1. Check required manifests & JSON syntax
    manifests = ["plugin.json", "agents.json", "openpack.json", "README.md", "HANDBOOK.md", "AGENTS.md"]
    for m in manifests:
        p = root / m
        if not p.exists():
            errors.append(f"Missing root manifest: {m}")
        else:
            if m.endswith(".json"):
                try:
                    with open(p, "r", encoding="utf-8") as jf:
                        json.load(jf)
                    print(f"  [OK] Valid JSON Manifest: {m}")
                except Exception as ex:
                    errors.append(f"Invalid JSON syntax in {m}: {ex}")
            else:
                print(f"  [OK] Root Document Present: {m}")

    # 2. Check all 14 rules (High-Level Agnostic + Low-Level Runtime)
    rules_dir = root / "rules"
    expected_rules = [
        # High-Level Agnostic Rules
        "ferrox-ddd-architecture.md",
        "ferrox-tdd-100-percent.md",
        "ferrox-sentinel-security.md",
        "ferrox-e2e-chaos-resilience.md",
        "ferrox-contract-governance.md",
        "ferrox-interop-connectors.md",
        "ferrox-polyglot-paradigms.md",
        "ferrox-e2e-contract-testing.md",
        # Low-Level Runtime Specific Rules
        "ferrox-rust-guidelines.md",
        "ferrox-wasm-guidelines.md",
        "ferrox-typescript-nestjs-guidelines.md",
        "ferrox-python-pyo3-guidelines.md",
        "ferrox-php-guidelines.md",
        "ferrox-java-loom-panama-guidelines.md"
    ]
    print(f"\n--- Checking {len(expected_rules)} Governing Rules ---")
    for r in expected_rules:
        p = rules_dir / r
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"Missing or empty rule: {r}")
        else:
            print(f"  [OK] Rule: {r} ({p.stat().st_size} bytes)")

    # 3. Check all 13 skills and YAML frontmatter
    skills_dir = root / "skills"
    expected_skills = [
        # High-Level Agnostic Skills
        "ferrox-ddd-planner",
        "ferrox-tdd-orchestrator",
        "ferrox-e2e-scaffolder",
        "ferrox-security-auditor",
        "ferrox-polyglot-connector",
        "ferrox-code-reviewer",
        "ferrox-workflow-handoff",
        # Low-Level Runtime Specific Skills
        "ferrox-rust-implementer",
        "ferrox-wasm-builder",
        "ferrox-nestjs-implementer",
        "ferrox-python-implementer",
        "ferrox-php-implementer",
        "ferrox-java-implementer"
    ]
    print(f"\n--- Checking {len(expected_skills)} Actionable Skills ---")
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
                print(f"  [OK] Skill with Valid Frontmatter: {s}")

    # 4. Check all 7 specialized agents
    agents_dir = root / "agents"
    expected_agents = [
        "ferrox-architect-ddd.md",
        "ferrox-tdd-engineer.md",
        "ferrox-security-sentinel.md",
        "ferrox-qa-chaos-engineer.md",
        "ferrox-rust-specialist.md",
        "ferrox-wasm-specialist.md",
        "ferrox-polyglot-implementer.md"
    ]
    print(f"\n--- Checking {len(expected_agents)} Specialized Agents ---")
    for a in expected_agents:
        p = agents_dir / a
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"Missing or empty agent spec: {a}")
        else:
            print(f"  [OK] Agent Persona: {a}")

    # 5. Check CLI tools
    scripts_dir = root / "scripts"
    expected_scripts = [
        "check_coverage.py",
        "run_wstg_security_scanner.py",
        "verify_toolkit.py",
        "install.ps1",
        "install.sh"
    ]
    print(f"\n--- Checking {len(expected_scripts)} CLI Tools & Installers ---")
    for sc in expected_scripts:
        p = scripts_dir / sc
        if not p.exists():
            errors.append(f"Missing script: {sc}")
        else:
            print(f"  [OK] Script / Installer: {sc}")

    print("\n============================================================")
    if errors:
        print(f"❌ Verification failed with {len(errors)} error(s):")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("✅ ALL FERROX AGENT TOOLKIT COMPONENTS SUCCESSFULLY VERIFIED!")
        print("============================================================\n")
        sys.exit(0)

if __name__ == "__main__":
    test_toolkit_integrity()

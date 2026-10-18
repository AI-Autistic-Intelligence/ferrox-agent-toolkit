#!/usr/bin/env python3
"""Ferrox Agent Toolkit CLI for Python & PyPI."""

import os
import sys
import shutil
from pathlib import Path

VERSION = "0.1.1"
ROOT_DIR = Path(__file__).resolve().parent.parent

HELP_TEXT = f"""
Ferrox Agent Toolkit CLI v{VERSION}
High-performance dual-layer AI agent architecture for modern polyglot engineering.

USAGE:
  ferrox-agent <command> [options]

COMMANDS:
  init [path]       Install / scaffold Ferrox agents and rules into a target workspace
  list              List all 10 specialized agents and 19 domain skills
  rules             Display the core Ferrox Master Operating Guide (AGENTS.md)
  verify            Verify toolkit integrity and directory layout
  version, -v       Show version
  help, -h          Show this help message

EXAMPLES:
  ferrox-agent init ./my-project
  ferrox-agent list
  ferrox-agent rules
"""


def handle_init(target_path=None):
    target = Path(target_path or ".").resolve()
    print(f"\033[36mInitializing Ferrox Agent Toolkit in: {target}\033[0m")

    agents_dir = target / ".agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    rules_src = ROOT_DIR / "rules"
    skills_src = ROOT_DIR / "skills"
    agents_src = ROOT_DIR / "agents"
    agents_md = ROOT_DIR / "AGENTS.md"

    if rules_src.exists():
        print("  -> Installing Layer 1 governance rules...")
        shutil.copytree(rules_src, agents_dir / "rules", dirs_exist_ok=True)
    if skills_src.exists():
        print("  -> Installing 19 domain engineering skills...")
        shutil.copytree(skills_src, agents_dir / "skills", dirs_exist_ok=True)
    if agents_src.exists():
        print("  -> Installing 10 specialized agent specs...")
        shutil.copytree(agents_src, agents_dir / "agents", dirs_exist_ok=True)
    if agents_md.exists():
        target_md = target / "AGENTS.md"
        if not target_md.exists():
            print("  -> Installing AGENTS.md operating guide...")
            shutil.copy2(agents_md, target_md)

    print("\033[32m✔ Ferrox Agent Toolkit successfully initialized!\033[0m\n")


def handle_list():
    print("\033[35m=== Ferrox Agent Toolkit Roster ===\033[0m\n")

    agents_path = ROOT_DIR / "agents"
    if agents_path.exists():
        print("\033[33m[Specialized Agents (10)]:\033[0m")
        for f in sorted(agents_path.glob("*.md")):
            print(f"  • {f.stem}")
        print()

    skills_path = ROOT_DIR / "skills"
    if skills_path.exists():
        print("\033[34m[Domain Skills (19)]:\033[0m")
        for d in sorted([s for s in skills_path.iterdir() if s.is_dir()]):
            print(f"  • {d.name}")
        print()


def handle_rules():
    agents_md = ROOT_DIR / "AGENTS.md"
    if agents_md.exists():
        print(agents_md.read_text(encoding="utf-8"))
    else:
        print("AGENTS.md not found.", file=sys.stderr)


def handle_verify():
    print("\033[36mVerifying Ferrox Agent Toolkit integrity...\033[0m")
    required = ["rules", "skills", "agents", "AGENTS.md", "plugin.json", "openpack.json"]
    all_ok = True
    for item in required:
        p = ROOT_DIR / item
        if p.exists():
            print(f"  \033[32m✔\033[0m {item}")
        else:
            print(f"  \033[31m✖ Missing:\033[0m {item}")
            all_ok = False
    if all_ok:
        print("\033[32mAll core components verified.\033[0m")
    else:
        sys.exit(1)


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "help"

    if cmd == "init":
        handle_init(args[1] if len(args) > 1 else None)
    elif cmd == "list":
        handle_list()
    elif cmd == "rules":
        handle_rules()
    elif cmd == "verify":
        handle_verify()
    elif cmd in ("version", "-v", "--version"):
        print(f"ferrox-agent v{VERSION}")
    elif cmd in ("help", "-h", "--help"):
        print(HELP_TEXT)
    else:
        print(HELP_TEXT)


if __name__ == "__main__":
    main()

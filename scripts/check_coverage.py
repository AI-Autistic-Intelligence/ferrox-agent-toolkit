#!/usr/bin/env python3
"""
Ferrox Ecosystem - Top-Level 100% Coverage Enforcer CLI
"""
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
coverage_script_path = script_dir.parent / "skills" / "ferrox-tdd-orchestrator" / "scripts"
sys.path.insert(0, str(coverage_script_path))

from check_coverage import main

if __name__ == "__main__":
    main()

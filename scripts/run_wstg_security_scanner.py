#!/usr/bin/env python3
"""
Ferrox Ecosystem - Top-Level WSTG Security Scanner CLI
Runs the Security Sentinel audit across all OWASP WSTG vectors.
"""
import sys
from pathlib import Path

# Add skills/ferrox-security-auditor/scripts to sys.path
script_dir = Path(__file__).resolve().parent
scanner_path = script_dir.parent / "skills" / "ferrox-security-auditor" / "scripts"
sys.path.insert(0, str(scanner_path))

from wstg_security_scanner import WstgSecurityScanner

if __name__ == "__main__":
    scanner = WstgSecurityScanner()
    report = scanner.run_all()
    sys.exit(0 if report["passed"] == report["total"] else 1)

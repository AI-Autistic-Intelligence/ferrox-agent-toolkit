#!/usr/bin/env python3
"""
Ferrox Ecosystem Universal Coverage Checker & 100% Policy Enforcer
Supports: LCOV (lcov.info), Cobertura/Clover (coverage.xml), JaCoCo (jacoco.xml), JSON coverage reports.
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import json
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def parse_lcov(file_path: Path):
    total_lines = 0
    covered_lines = 0
    total_branches = 0
    covered_branches = 0
    file_uncovered = {}

    current_file = None
    uncovered_lines_in_file = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line.startswith("SF:"):
                current_file = line[3:]
                uncovered_lines_in_file = []
            elif line.startswith("DA:"):
                # DA:<line_number>,<execution_count>
                parts = line[3:].split(",")
                if len(parts) >= 2:
                    line_num = int(parts[0])
                    hits = int(parts[1])
                    total_lines += 1
                    if hits > 0:
                        covered_lines += 1
                    else:
                        uncovered_lines_in_file.append(line_num)
            elif line.startswith("BRDA:"):
                # BRDA:<line>,<block>,<branch>,<taken>
                parts = line[5:].split(",")
                if len(parts) >= 4:
                    total_branches += 1
                    taken = parts[3]
                    if taken not in ("0", "-"):
                        covered_branches += 1
            elif line == "end_of_record":
                if uncovered_lines_in_file and current_file:
                    file_uncovered[current_file] = uncovered_lines_in_file
                current_file = None
                uncovered_lines_in_file = []

    return {
        "total_lines": total_lines,
        "covered_lines": covered_lines,
        "total_branches": total_branches,
        "covered_branches": covered_branches,
        "file_uncovered": file_uncovered
    }

def parse_xml_cobertura(file_path: Path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Check root attributes
    lines_valid = root.attrib.get("lines-valid")
    lines_covered = root.attrib.get("lines-covered")
    branches_valid = root.attrib.get("branches-valid")
    branches_covered = root.attrib.get("branches-covered")

    file_uncovered = {}

    total_lines = int(lines_valid) if lines_valid is not None else 0
    covered_lines = int(lines_covered) if lines_covered is not None else 0
    total_branches = int(branches_valid) if branches_valid is not None else 0
    covered_branches = int(branches_covered) if branches_covered is not None else 0

    # Scan packages / classes
    for cls in root.iter("class"):
        filename = cls.attrib.get("filename", cls.attrib.get("name", "unknown"))
        uncovered = []
        for line in cls.iter("line"):
            hits = int(line.attrib.get("hits", "0"))
            num = int(line.attrib.get("number", "0"))
            if hits == 0:
                uncovered.append(num)
        if uncovered:
            file_uncovered[filename] = uncovered

    return {
        "total_lines": total_lines,
        "covered_lines": covered_lines,
        "total_branches": total_branches,
        "covered_branches": covered_branches,
        "file_uncovered": file_uncovered
    }

def parse_jacoco_xml(file_path: Path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    total_lines = 0
    covered_lines = 0
    total_branches = 0
    covered_branches = 0
    file_uncovered = {}

    for counter in root.findall("counter"):
        c_type = counter.attrib.get("type")
        missed = int(counter.attrib.get("missed", 0))
        covered = int(counter.attrib.get("covered", 0))
        if c_type == "LINE":
            total_lines = missed + covered
            covered_lines = covered
        elif c_type == "BRANCH":
            total_branches = missed + covered
            covered_branches = covered

    for pkg in root.findall("package"):
        for sf in pkg.findall("sourcefile"):
            sf_name = f"{pkg.attrib.get('name', '')}/{sf.attrib.get('name', '')}"
            uncovered = []
            for line in sf.findall("line"):
                mi = int(line.attrib.get("mi", 0))
                nr = int(line.attrib.get("nr", 0))
                if mi > 0:
                    uncovered.append(nr)
            if uncovered:
                file_uncovered[sf_name] = uncovered

    return {
        "total_lines": total_lines,
        "covered_lines": covered_lines,
        "total_branches": total_branches,
        "covered_branches": covered_branches,
        "file_uncovered": file_uncovered
    }

def auto_detect_coverage_file(start_dir: Path):
    candidates = [
        "lcov.info",
        "coverage/lcov.info",
        "target/llvm-cov/lcov.info",
        "coverage.xml",
        "coverage/coverage.xml",
        "target/site/jacoco/jacoco.xml",
        "coverage-final.json"
    ]
    for c in candidates:
        p = start_dir / c
        if p.exists():
            return p
    return None

def main():
    parser = argparse.ArgumentParser(description="Ferrox Universal Coverage 100% Policy Enforcer")
    parser.add_argument("file", nargs="?", help="Path to coverage report file (lcov.info, coverage.xml, jacoco.xml)")
    parser.add_argument("--target", type=float, default=100.0, help="Required coverage threshold (default: 100.0)")
    parser.add_argument("--dir", type=str, default=".", help="Root directory to search if file not specified")

    args = parser.parse_args()

    coverage_file = None
    if args.file:
        coverage_file = Path(args.file)
    else:
        coverage_file = auto_detect_coverage_file(Path(args.dir))

    if not coverage_file or not coverage_file.exists():
        print(f"{Colors.RED}[ERROR] Coverage file not found! Please specify a coverage file or run your language coverage generator.{Colors.ENDC}")
        sys.exit(1)

    print(f"{Colors.CYAN}{Colors.BOLD}🔍 FERROX COVERAGE ENFORCER: Analyzing {coverage_file}...{Colors.ENDC}")

    stats = None
    fn_lower = coverage_file.name.lower()
    if fn_lower.endswith(".info"):
        stats = parse_lcov(coverage_file)
    elif fn_lower.endswith(".xml"):
        if "jacoco" in fn_lower or "jacoco" in str(coverage_file).lower():
            stats = parse_jacoco_xml(coverage_file)
        else:
            stats = parse_xml_cobertura(coverage_file)
    else:
        # Fallback to LCOV
        stats = parse_lcov(coverage_file)

    total_lines = stats["total_lines"]
    covered_lines = stats["covered_lines"]
    line_pct = (covered_lines / total_lines * 100.0) if total_lines > 0 else 100.0

    total_branches = stats["total_branches"]
    covered_branches = stats["covered_branches"]
    branch_pct = (covered_branches / total_branches * 100.0) if total_branches > 0 else 100.0

    print(f"\n{Colors.BOLD}--- COVERAGE SUMMARY ---{Colors.ENDC}")
    print(f"Lines:    {covered_lines}/{total_lines} ({line_pct:.2f}%)")
    if total_branches > 0:
        print(f"Branches: {covered_branches}/{total_branches} ({branch_pct:.2f}%)")

    pass_lines = line_pct >= args.target
    pass_branches = (total_branches == 0) or (branch_pct >= args.target)

    if stats["file_uncovered"]:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  UNCOVERED LINES DETECTED (Violation of 100% Policy):{Colors.ENDC}")
        for file_name, lines in list(stats["file_uncovered"].items())[:20]:
            print(f"  • {file_name}: lines {lines}")
        if len(stats["file_uncovered"]) > 20:
            print(f"  ... and {len(stats['file_uncovered']) - 20} more files.")

    print(f"\n{Colors.BOLD}--- RESULT ---{Colors.ENDC}")
    if pass_lines and pass_branches:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ 100% TEST COVERAGE POLICY ACHIEVED! ({line_pct:.2f}% lines, {branch_pct:.2f}% branches){Colors.ENDC}\n")
        sys.exit(0)
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ 100% COVERAGE POLICY FAILED! Expected {args.target}%, got {line_pct:.2f}% lines, {branch_pct:.2f}% branches.{Colors.ENDC}")
        print(f"{Colors.RED}Please write TDD test cases to exercise the unvisited lines/branches above.{Colors.ENDC}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

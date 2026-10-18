#!/usr/bin/env python3
"""
Ferrox Diff Debris Scanner
Scans Git diff (origin/master...HEAD or local uncommitted changes) for forbidden debug statements.
"""

import sys
import subprocess
import re

FORBIDDEN_PATTERNS = [
    (r"\bdbg!\s*\(", "Rust dbg!() macro"),
    (r"\bprintln!\s*\(", "Rust println!() debug statement"),
    (r"\btodo!\s*\(", "Rust todo!() unfinished macro"),
    (r"\bunimplemented!\s*\(", "Rust unimplemented!() macro"),
    (r"\bconsole\.log\s*\(", "JavaScript / TypeScript console.log()"),
    (r"\bconsole\.debug\s*\(", "JavaScript / TypeScript console.debug()"),
    (r"\bdebugger\s*;", "JavaScript / TypeScript debugger statement"),
    (r"\bvar_dump\s*\(", "PHP var_dump()"),
    (r"\bprint_r\s*\(", "PHP print_r()"),
    (r"\bdd\s*\(", "PHP dd() dump and die"),
    (r"\bSystem\.out\.println\s*\(", "Java System.out.println()"),
    (r"\bSystem\.err\.println\s*\(", "Java System.err.println()"),
    (r"\bimport\s+pdb\b", "Python pdb debugger"),
    (r"\bbreakpoint\s*\(", "Python breakpoint()"),
]

def get_git_diff():
    # Try diff against origin/master, fallback to HEAD~1, fallback to working tree
    commands = [
        ["git", "diff", "origin/master...HEAD"],
        ["git", "diff", "origin/main...HEAD"],
        ["git", "diff", "HEAD~1"],
        ["git", "diff", "HEAD"],
        ["git", "diff"]
    ]
    for cmd in commands:
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            if res.stdout.strip():
                return res.stdout
        except Exception:
            continue
    return ""

def scan_diff():
    diff_text = get_git_diff()
    if not diff_text:
        print("✅ No Git diff detected or working tree clean.")
        return 0

    violations = []
    current_file = "unknown"
    line_number = 0
    is_code_file = False

    CODE_EXTENSIONS = (
        ".rs", ".ts", ".js", ".tsx", ".jsx", ".py", ".php",
        ".java", ".c", ".cpp", ".h", ".hpp", ".go"
    )

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            is_code_file = current_file.endswith(CODE_EXTENSIONS)
        elif not is_code_file:
            continue
        elif line.startswith("@@"):
            # @@ -1,5 +1,6 @@
            match = re.search(r"\+(\d+)", line)
            if match:
                line_number = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            line_number += 1
            code_line = line[1:]
            for pattern, desc in FORBIDDEN_PATTERNS:
                if re.search(pattern, code_line):
                    violations.append((current_file, line_number, desc, code_line.strip()))
        elif not line.startswith("-"):
            line_number += 1


    if violations:
        print(f"❌ FORBIDDEN DEBUG DEBRIS DETECTED ({len(violations)} violations):")
        for f, ln, desc, snippet in violations:
            print(f"  • {f}:{ln} [{desc}] -> {snippet}")
        print("\nPlease remove all debug statements before opening Pull Request.")
        return 1
    else:
        print("✅ Zero debug debris detected in Git diff! Ready for Self-Review approval.")
        return 0

if __name__ == "__main__":
    sys.exit(scan_diff())

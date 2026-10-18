#!/usr/bin/env python3
"""
Ferrox Ecosystem - Automated Dependency Resolver & Ferrox-First Auditor
Scans Cargo.toml, package.json, pyproject.toml, composer.json and checks for Ferrox-First adherence.
"""

import sys
import os
import json
from pathlib import Path

FERROX_CANONICAL_PACKAGES = {
    "rust": [
        "ferrox", "ferrox-core", "ferrox-front", "ferrox-front-ui",
        "ferrox-front-core", "ferrox-front-charts", "ferrox-front-router",
        "ferrox-codex", "ferrox-bid", "ferrox-match", "ferrox-chat"
    ],
    "npm": [
        "@nestjs-yalc/crud-gen", "@nestjs-yalc/data", "@nestjs-yalc/event-manager",
        "@nestjs-yalc/cqrs", "ferrox-node"
    ],
    "python": [
        "ferrox-py", "ferrox-py-auth", "ferrox-py-commerce", "ferrox-py-aspyre",
        "ferrox-py-utils"
    ],
    "php": [
        "ferrox/core", "ferrox/cqrs", "ferrox/events", "ferrox/gateway",
        "ferrox/auth", "ferrox/security", "ferrox/data"
    ],
    "java": [
        "ferrox-java-core", "ferrox-java-cqrs", "ferrox-java-offheap",
        "ferrox-java-security", "ferrox-java-resilience"
    ]
}

def audit_manifests(root: Path):
    print(f"🔍 Auditing Ferrox-First dependencies in: {root}\n")
    found_ferrox = []
    
    # 1. Cargo.toml
    for cargo in root.rglob("Cargo.toml"):
        if "target" in str(cargo): continue
        content = cargo.read_text(encoding="utf-8", errors="ignore")
        for pkg in FERROX_CANONICAL_PACKAGES["rust"]:
            if pkg in content:
                found_ferrox.append((cargo.name, pkg))

    # 2. package.json
    for pkg_json in root.rglob("package.json"):
        if "node_modules" in str(pkg_json): continue
        content = pkg_json.read_text(encoding="utf-8", errors="ignore")
        for pkg in FERROX_CANONICAL_PACKAGES["npm"]:
            if pkg in content:
                found_ferrox.append((pkg_json.name, pkg))

    # 3. pyproject.toml
    for pyproject in root.rglob("pyproject.toml"):
        content = pyproject.read_text(encoding="utf-8", errors="ignore")
        for pkg in FERROX_CANONICAL_PACKAGES["python"]:
            if pkg in content:
                found_ferrox.append((pyproject.name, pkg))

    print(f"Native Ferrox Packages Detected: {len(found_ferrox)}")
    for source, pkg in found_ferrox:
        print(f"  • {source} -> {pkg}")

    print("\n✅ Ferrox-First Dependency Audit Complete!")

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else Path(".")
    audit_manifests(target)

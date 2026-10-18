#!/usr/bin/env bash
# Ferrox Agent Toolkit - Bash Installer for Linux / macOS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "  🛡️  FERROX AGENT TOOLKIT INSTALLER (POSIX)"
echo "============================================================"
echo "Source: $TOOLKIT_ROOT"

PLUGIN_TARGET="$HOME/.gemini/config/plugins/ferrox-agent-toolkit"
echo "Target: $PLUGIN_TARGET"

mkdir -p "$PLUGIN_TARGET"
rm -rf "$PLUGIN_TARGET"/*

cp -r "$TOOLKIT_ROOT"/plugin.json "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/agents.json "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/openpack.json "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/README.md "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/HANDBOOK.md "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/AGENTS.md "$PLUGIN_TARGET"/

cp -r "$TOOLKIT_ROOT"/rules "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/skills "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/agents "$PLUGIN_TARGET"/
cp -r "$TOOLKIT_ROOT"/scripts "$PLUGIN_TARGET"/

echo "============================================================"
echo "  ✅ FERROX AGENT TOOLKIT SUCCESSFULLY INSTALLED!"
echo "============================================================"

#!/usr/bin/env bash
# Ferrox Agent Toolkit - Bash Installer for Linux / macOS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "  🛡️  FERROX AGENT TOOLKIT INSTALLER (POSIX)"
echo "============================================================"
echo "Source: $TOOLKIT_ROOT"

TARGET="${1:-all}"
WORKSPACE_DIR="${2:-$(dirname "$TOOLKIT_ROOT")}"

echo "Mode:   $TARGET"

if [ "$TARGET" = "all" ] || [ "$TARGET" = "antigravity" ]; then
    PLUGIN_TARGET="$HOME/.gemini/config/plugins/ferrox-agent-toolkit"
    echo "Target Plugin: $PLUGIN_TARGET"

    mkdir -p "$PLUGIN_TARGET"
    rm -rf "$PLUGIN_TARGET"/*

    cp -r "$TOOLKIT_ROOT"/plugin.json "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/agents.json "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/openpack.json "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/README.md "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/HANDBOOK.md "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/AGENTS.md "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/LICENSE "$PLUGIN_TARGET"/

    cp -r "$TOOLKIT_ROOT"/rules "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/skills "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/agents "$PLUGIN_TARGET"/
    cp -r "$TOOLKIT_ROOT"/scripts "$PLUGIN_TARGET"/
    echo "  -> Antigravity Plugin successfully updated."
fi

if [ "$TARGET" = "all" ] || [ "$TARGET" = "workspace" ]; then
    echo "Target Workspace: $WORKSPACE_DIR"
    mkdir -p "$WORKSPACE_DIR/.agents"

    ln -sfn "$TOOLKIT_ROOT/rules" "$WORKSPACE_DIR/.agents/rules"
    ln -sfn "$TOOLKIT_ROOT/skills" "$WORKSPACE_DIR/.agents/skills"
    ln -sfn "$TOOLKIT_ROOT/agents" "$WORKSPACE_DIR/.agents/agents"
    cp "$TOOLKIT_ROOT/AGENTS.md" "$WORKSPACE_DIR/AGENTS.md"

    echo "  -> Workspace .agents/ linked and AGENTS.md copied to $WORKSPACE_DIR."
fi

echo "============================================================"
echo "  ✅ FERROX AGENT TOOLKIT SUCCESSFULLY INSTALLED!"
echo "============================================================"

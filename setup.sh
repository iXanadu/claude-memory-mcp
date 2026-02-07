#!/usr/bin/env bash
#
# setup.sh — Register claude-memory MCP server for the current user
#
# Prerequisites:
#   - pyenv + pyenv-virtualenv installed
#   - pyenv virtualenv 'cc-memory-3.12' already created and deps installed
#     (run install.sh first if not)
#   - claude CLI available in PATH
#
# Usage:
#   ./setup.sh              # register MCP server
#   ./setup.sh --uninstall  # remove MCP server registration
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_NAME="cc-memory-3.12"
PYTHON_BIN="$(pyenv prefix "$VENV_NAME")/bin/python"

if [[ "${1:-}" == "--uninstall" ]]; then
    echo "Removing claude-memory MCP server registration..."
    claude mcp remove claude-memory 2>/dev/null && echo "Done." || echo "Not registered."
    exit 0
fi

# Verify the virtualenv exists and has the package
if ! "$PYTHON_BIN" -c "import claude_memory_mcp" 2>/dev/null; then
    echo "ERROR: pyenv virtualenv '$VENV_NAME' missing or claude-memory-mcp not installed."
    echo "Run install.sh first:"
    echo "  cd $PROJECT_DIR && ./install.sh"
    exit 1
fi

# Remove existing registration if present, then re-register
echo "Registering claude-memory MCP server for user $(whoami)..."
claude mcp remove claude-memory 2>/dev/null || true
claude mcp add claude-memory --scope user -- "$PYTHON_BIN" -m claude_memory_mcp.server

echo ""
echo "Done. The memory tools will be available in your next Claude Code session."
echo "Verify with: claude mcp list"

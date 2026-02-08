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

# Read .env file and build -e flags for claude mcp add
ENV_FLAGS=()
ENV_FILE="$PROJECT_DIR/.env"
if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line; do
        # Skip comments and blank lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue
        ENV_FLAGS+=(-e "$line")
    done < "$ENV_FILE"
    echo "Loaded env from .env: ${ENV_FLAGS[*]}"
else
    echo "No .env file found — using defaults (localhost:8920)."
fi

# Remove existing registration if present, then re-register
echo "Registering claude-memory MCP server for user $(whoami)..."
claude mcp remove claude-memory 2>/dev/null || true
claude mcp add claude-memory --scope user ${ENV_FLAGS[@]+"${ENV_FLAGS[@]}"} -- "$PYTHON_BIN" -m claude_memory_mcp.server

# Install/update global CLAUDE.md (teaches Claude how to use memory tools)
GLOBAL_CLAUDE="$HOME/.claude/CLAUDE.md"
TEMPLATE_CLAUDE="$PROJECT_DIR/templates/GLOBAL_CLAUDE.md"
if [[ ! -f "$GLOBAL_CLAUDE" ]]; then
    mkdir -p "$HOME/.claude"
    cp "$TEMPLATE_CLAUDE" "$GLOBAL_CLAUDE"
    echo "Installed global CLAUDE.md to $GLOBAL_CLAUDE"
elif ! diff -q "$TEMPLATE_CLAUDE" "$GLOBAL_CLAUDE" >/dev/null 2>&1; then
    echo ""
    echo "NOTE: $GLOBAL_CLAUDE differs from template."
    echo "  To update: cp $TEMPLATE_CLAUDE $GLOBAL_CLAUDE"
else
    echo "Global CLAUDE.md is up to date."
fi

echo ""
echo "Done. The memory tools will be available in your next Claude Code session."
echo "Verify with: claude mcp list"

#!/usr/bin/env bash
#
# install.sh — Create pyenv virtualenv and install claude-memory-mcp
#
# Prerequisites:
#   - pyenv + pyenv-virtualenv installed
#   - Python 3.12.x installed via pyenv (pyenv install 3.12)
#
# Usage:
#   ./install.sh
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_NAME="cc-memory-3.12"

# Find the installed 3.12.x version
PY_VERSION=$(pyenv versions --bare | grep '^3\.12\.' | head -1)
if [[ -z "$PY_VERSION" ]]; then
    echo "ERROR: No Python 3.12.x found in pyenv."
    echo "Install one first: pyenv install 3.12"
    exit 1
fi

# Create virtualenv if it doesn't exist
if pyenv prefix "$VENV_NAME" &>/dev/null; then
    echo "pyenv virtualenv '$VENV_NAME' already exists."
else
    echo "Creating pyenv virtualenv '$VENV_NAME' from Python $PY_VERSION..."
    pyenv virtualenv "$PY_VERSION" "$VENV_NAME"
fi

# Set local version
cd "$PROJECT_DIR"
pyenv local "$VENV_NAME"

# Install package and dependencies
echo "Installing claude-memory-mcp..."
PYTHON_BIN="$(pyenv prefix "$VENV_NAME")/bin/python"
"$PYTHON_BIN" -m pip install -e ".[dev]" --quiet

echo ""
echo "Installed. Now run setup.sh to register with Claude Code:"
echo "  cd $PROJECT_DIR && ./setup.sh"

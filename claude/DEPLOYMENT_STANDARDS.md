# claude-memory-mcp — Deployment Standards

## Overview

This is a **local MCP server** — not a web service, not a daemon. It runs as a subprocess spawned by Claude Code on demand via stdio transport. There is no server to manage, no port to configure, no process to monitor.

---

## Installation

```bash
# One-time setup
cd /opt/srv/claude-memory-mcp
./install.sh      # Creates pyenv virtualenv, installs dependencies
cp .env.example .env  # Configure (usually defaults are fine)
./setup.sh        # Registers MCP server with Claude Code
```

## Updating

```bash
cd /opt/srv/claude-memory-mcp
git pull origin main
./install.sh      # Reinstall in case dependencies changed
```

No restart needed — Claude Code spawns a fresh process each session.

## Uninstalling

```bash
cd /opt/srv/claude-memory-mcp
./setup.sh --uninstall    # Removes MCP registration
```

---

## Configuration

Via `.env` file (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMORY_API_URL` | `http://localhost:8920` | ha-semantic-memory endpoint |
| `MEMORY_API_TOKEN` | *(empty)* | Bearer token (must match `HAMEM_API_TOKEN`) |
| `MEMORY_DEFAULT_SCOPE` | `machine` | Default scope when not specified |

---

## Prerequisites

- **ha-semantic-memory** must be running on the configured port (default 8920)
- **Python 3.12+** via pyenv
- **Claude Code CLI** installed (for `claude mcp add`)

---

## Verification

```bash
# Check MCP registration
claude mcp list

# Run tests
pytest tests/ -v

# Check backend connectivity (requires ha-semantic-memory running)
curl http://localhost:8920/health
```

---

## Multi-Machine Setup

To use on a new machine:
1. Clone the repo to `/opt/srv/claude-memory-mcp/`
2. Run `./install.sh` and `./setup.sh`
3. Ensure ha-semantic-memory is accessible (update `MEMORY_API_URL` if remote)
4. Shared-scope memories sync automatically via the shared backend

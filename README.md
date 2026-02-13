> [!WARNING]
> **This project has been deprecated and archived.**
>
> All functionality has been merged into **[engram](https://github.com/iXanadu/engram)** — a general-purpose semantic memory service for AI agents.
>
> - MCP server code → `engram/integrations/claude-code/` (package: `engram-mcp`)
> - Backend server → `engram/server/`
>
> This repo will not receive further updates. Please use engram for new installations.

---

# claude-memory-mcp (Archived)

MCP server that gives [Claude Code](https://docs.anthropic.com/en/docs/claude-code) persistent semantic memory across sessions, projects, and machines.

Wraps [ha-semantic-memory](https://github.com/iXanadu/ha-semantic-memory) (FastAPI + pgvector + Ollama embeddings) as a set of MCP tools that Claude Code can call directly.

## Why

- **Crash recovery** — session progress is saved incrementally, so a disconnected terminal doesn't mean lost work
- **Cross-session continuity** — lessons learned in one conversation carry forward to the next
- **Fleet-wide knowledge** — multiple Claude Code instances on different machines can share a common memory pool

## Architecture

```
Claude Code  ──stdio──>  claude-memory-mcp (this project)
                              ↕ HTTP (httpx)
                         ha-semantic-memory (FastAPI, port 8920)
                              ↕ asyncpg + pgvector
                         PostgreSQL 17
```

This project is a thin MCP client. All storage, embedding, and search logic lives in ha-semantic-memory.

## Security Model

Security uses two layers — **network isolation** and an **optional API token**:

**Network layer (primary):**
- **Single machine (simplest):** ha-semantic-memory binds to `localhost` — only local processes can connect. This is the default.
- **Multi-machine fleet:** Use [Tailscale](https://tailscale.com/) (or another VPN/overlay network) so that only your machines can reach the API.
- **Never expose port 8920 to the public internet.**

**API token (defense in depth):**

ha-semantic-memory supports an optional bearer token. When `HAMEM_API_TOKEN` is set on the server, all clients must send a matching `Authorization: Bearer <token>` header. Failed auth attempts are logged at WARNING level with the client IP and endpoint — easy to spot in logs.

To enable:
1. Set `HAMEM_API_TOKEN=your-secret-here` in ha-semantic-memory's `.env`
2. Set `MEMORY_API_TOKEN=your-secret-here` in this project's `.env`
3. Restart both services

With no token set (the default), the API is unauthenticated — secured by network perimeter alone. Health checks (`/health`) always bypass auth so monitoring still works.

## Prerequisites

- [ha-semantic-memory](https://github.com/iXanadu/ha-semantic-memory) running and accessible (default: `http://localhost:8920`)
- [pyenv](https://github.com/pyenv/pyenv) + [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- Python 3.12+ installed via pyenv (`pyenv install 3.12`)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

## Quick Start

```bash
# Create shared services directory (first time only)
sudo mkdir -p /opt/srv
sudo chown $(whoami):staff /opt/srv    # macOS — use $(whoami):$(whoami) on Linux

# Clone
git clone https://github.com/iXanadu/claude-memory-mcp.git /opt/srv/claude-memory-mcp
cd /opt/srv/claude-memory-mcp

# Install (creates pyenv virtualenv, installs dependencies)
./install.sh

# Register MCP server for your user
./setup.sh

# Verify
claude mcp list
# claude-memory: ... ✓ Connected
```

Start a new Claude Code session — the five memory tools will be available automatically.

## Configuration

Configuration is via environment variables in a `.env` file. `setup.sh` reads this file and passes the values to Claude Code's MCP config automatically.

```bash
cp .env.example .env
# Edit .env with your values, then re-run setup.sh
./setup.sh
```

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMORY_API_URL` | `http://localhost:8920` | ha-semantic-memory API endpoint |
| `MEMORY_API_TOKEN` | *(empty)* | Optional bearer token (must match `HAMEM_API_TOKEN` on server) |
| `MEMORY_DEFAULT_SCOPE` | `machine` | Default scope when none specified |

The `.env` file is gitignored — host-specific values never enter the repo.

For multi-machine setups, point `MEMORY_API_URL` at the hostname or Tailscale IP of the machine running ha-semantic-memory (e.g. `http://macmini:8920`). See [Security Model](#security-model) — never use a public IP.

**Note:** This project does not hold any database credentials. PostgreSQL and Ollama connection details are configured in ha-semantic-memory itself (see its `HAMEM_*` env vars).

## Tools

| Tool | Description |
|------|-------------|
| `memory_store` | Save a memory with a key, value, optional tags, and scope |
| `memory_search` | Semantic search across stored memories |
| `memory_get` | Retrieve a specific memory by exact key |
| `memory_forget` | Delete a specific memory by exact key |
| `memory_status` | Check health of the memory backend |

## Scoping

Memories are isolated by scope using ha-semantic-memory's `user_id` field:

| Scope | user_id | Use case |
|-------|---------|----------|
| `machine` | `cc-{hostname}` | Machine-specific context (paths, services, env) |
| `shared` | `cc-shared` | Knowledge useful to all Claude Code instances |
| `project` | `cc-proj-{dirname}` | Project-specific patterns and decisions |

Default is `machine`. Every tool accepts an optional `scope` parameter to override.

## Multi-User Setup

The project lives in a shared location (`/opt/srv/`). Each OS user registers the MCP server independently:

```bash
cd /opt/srv/claude-memory-mcp
./setup.sh              # registers for current user
./setup.sh --uninstall  # removes registration
```

The pyenv virtualenv (`cc-memory-3.12`) is shared — `setup.sh` just points each user's `~/.claude.json` at it.

## Development

```bash
cd /opt/srv/claude-memory-mcp

# Run tests (all mocked, no running services required)
pytest tests/ -v

# Run against live ha-semantic-memory
MEMORY_API_URL=http://localhost:8920 python -m claude_memory_mcp.server
```

## Project Structure

```
├── install.sh                      # Create pyenv virtualenv + install deps
├── setup.sh                        # Register/unregister MCP server per user
├── pyproject.toml
├── .env.example                    # Configuration template
├── src/claude_memory_mcp/
│   ├── server.py                   # FastMCP server, 5 tool definitions
│   ├── client.py                   # httpx wrapper for ha-semantic-memory API
│   ├── scoping.py                  # Scope → user_id resolution
│   └── config.py                   # pydantic-settings configuration
└── tests/
    ├── test_server.py              # MCP tool integration tests
    ├── test_client.py              # API client unit tests
    └── test_scoping.py             # Scope resolution tests
```

## License

MIT

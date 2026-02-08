# claude-memory-mcp

MCP (Model Context Protocol) server that wraps ha-semantic-memory as persistent memory tools for Claude Code. Enables cross-session, cross-project, and cross-machine memory.

## Project Structure
- `src/claude_memory_mcp/` — MCP server source
  - `server.py` — FastMCP server with 5 tool definitions
  - `client.py` — Async httpx client for ha-semantic-memory API
  - `scoping.py` — Scope resolution (machine/shared/project → user_id)
  - `config.py` — Pydantic settings (env vars)
- `tests/` — pytest suite (25 tests: server, client, scoping)
- `install.sh` — Create pyenv virtualenv, install dependencies
- `setup.sh` — Register MCP server with Claude Code

## Key Commands
- Run tests: `pytest tests/ -v`
- Install: `./install.sh`
- Register MCP: `./setup.sh`
- Unregister: `./setup.sh --uninstall`

## Architecture
```
Claude Code → claude-memory-mcp (stdio) → ha-semantic-memory (HTTP :8920) → PostgreSQL
```

## MCP Tools
| Tool | Description |
|------|-------------|
| `memory_store` | Store a memory with key, value, tags, scope |
| `memory_search` | Semantic search with configurable limit |
| `memory_get` | Retrieve by exact key |
| `memory_forget` | Delete by exact key |
| `memory_status` | Health check of memory backend |

## Scoping Model
| Scope | user_id | Use for |
|-------|---------|---------|
| `machine` | `cc-{hostname}` | Machine-specific context (default) |
| `shared` | `cc-shared` | Cross-machine knowledge |
| `project` | `cc-proj-{dirname}` | Project-specific state |

## Conventions
- Python environment: pyenv virtualenv `cc-memory-3.12`
- Config via env vars in `.env` (see `.env.example`)
- Depends on ha-semantic-memory running on port 8920
- MCP transport: stdio (registered per-user via `claude mcp add`)

## Session State
- `claude/CODEBASE_STATE.md` — current technical state and recent work
- `claude/CONTEXT_MEMORY.md` — working context, decisions, priorities
- `claude/DEPLOYMENT_STANDARDS.md` — installation and registration workflow
- `claude/session_progress/` — per-session work logs

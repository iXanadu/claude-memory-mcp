# claude-memory-mcp — Codebase State

**Last Updated:** 2026-02-11
**Version:** 0.1.0 (93412ee)
**Status:** Production — Stable

---

## Project Overview

MCP server that wraps ha-semantic-memory as persistent memory tools for Claude Code. Provides 5 tools (store, search, get, forget, status) with 3 scoping levels (machine, shared, project). Runs as a stdio transport MCP server registered per-user.

**Architecture:**
```
Claude Code → claude-memory-mcp (stdio) → ha-semantic-memory (HTTP :8920) → PostgreSQL + pgvector
```

---

## Current State

- **25 tests passing** (14 server + 5 client + 6 scoping)
- **Production**: Registered as MCP server, actively used by Claude Code sessions
- **10 commits**: All work through empty-query fix + version traceability
- **Verified on MacMini**: Version reports `0.1.0 (93412ee)`, ready for multi-machine deployment

---

## Recent Major Work

- **2026-02-11**: Fixed empty query string causing 422 error in `memory_search` — now returns "No memories found." gracefully. Added git commit hash to `memory_status` output for build traceability (`Server version: 0.1.0 (hash)`). Verified both fixes in production.
- **2026-02-08**: Rewrote global CLAUDE.md memory scoping docs — fixed peer confusion about scope isolation, project resolution, and search behavior. Added `templates/GLOBAL_CLAUDE.md` as canonical master; `setup.sh` now deploys it to `~/.claude/CLAUDE.md`. Added machine scope to startup search pattern.
- **2026-02-07**: Added Claude Code working structure (.claude/CLAUDE.md, startup/wrapup commands, state files)
- **Initial implementation**: MCP server with 5 tools, 3-scope model, httpx async client
- **Install/setup fixes**: pyenv virtualenv detection, .env integration for MCP registration
- **Quick Start fix**: Added `/opt/srv` directory setup step to README

---

## Next Planned Work

- **Deploy to other machines** — clone, install, configure `MEMORY_API_URL` to point at MacMini
- Add `memory_list` tool (list all keys for a scope)
- Add `memory_update` tool (partial value updates)
- Improve error messages when ha-semantic-memory is unreachable
- Add connection retry logic

---

## Testing Status

| Suite | Count | Status |
|-------|-------|--------|
| Server (MCP tools) | 14 | Pass |
| Client (httpx) | 5 | Pass |
| Scoping (user_id resolution) | 6 | Pass |
| **Total** | **25** | **All passing** |

Run: `pytest tests/ -v`

---

## Key Files

| File | Purpose |
|------|---------|
| `src/claude_memory_mcp/server.py` | FastMCP server, 5 tool definitions |
| `src/claude_memory_mcp/client.py` | Async httpx client for ha-semantic-memory |
| `src/claude_memory_mcp/scoping.py` | Scope → user_id resolution |
| `src/claude_memory_mcp/config.py` | Pydantic settings (env vars) |
| `install.sh` | Create virtualenv, install deps |
| `setup.sh` | Register/unregister MCP with Claude Code, deploy global CLAUDE.md |
| `templates/GLOBAL_CLAUDE.md` | Canonical global CLAUDE.md (cp to ~/.claude/CLAUDE.md) |

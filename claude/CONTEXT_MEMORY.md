# claude-memory-mcp — Context Memory

**Last Updated:** 2026-02-07
**Status:** Stable / Maintenance

---

## Current Focus

Project is stable and in production. No active development. Available for enhancements as needed.

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| MCP stdio transport | Standard for Claude Code tool servers; simple process lifecycle |
| 3-scope model (machine/shared/project) | Balances isolation with knowledge sharing across contexts |
| httpx async client | Matches FastMCP's async model; connection pooling built-in |
| Thin wrapper pattern | All intelligence in ha-semantic-memory; this is just a transport adapter |
| Optional bearer token | Security layer inherited from ha-semantic-memory; configured via .env |
| pyenv virtualenv `cc-memory-3.12` | Follows project convention; isolated from system Python |

---

## Environment

| Item | Value |
|------|-------|
| Python | 3.12 (pyenv virtualenv `cc-memory-3.12`) |
| Location | `/opt/srv/claude-memory-mcp/` |
| Transport | stdio (registered via `claude mcp add`) |
| Backend | ha-semantic-memory on port 8920 |
| Config | `.env` file (see `.env.example`) |

---

## Dependencies

- **Upstream**: ha-semantic-memory (must be running on port 8920)
- **Downstream**: Claude Code sessions (via MCP protocol)

---

## Known Issues

- If ha-semantic-memory is not running, all tools return connection errors (no retry logic)
- The `setup.sh` script uses `claude mcp add` which requires Claude Code CLI to be installed

---

## Notes

- Test count in README previously said 26 — that was ha-semantic-memory's count, not this project's (25)
- The `.python-version` file points to `cc-memory-3.12` virtualenv and is gitignored

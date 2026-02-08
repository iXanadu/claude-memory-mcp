# Specifications

## MCP Tool Definitions

This server exposes 5 tools via the Model Context Protocol:

### `memory_store`
Store a persistent memory.
- **Parameters**: `key` (required), `value` (required), `tags` (optional), `scope` (optional)
- **Returns**: Confirmation message

### `memory_search`
Semantic search across memories.
- **Parameters**: `query` (required), `limit` (optional, default 5), `scope` (optional)
- **Returns**: Formatted list of matching memories with scores

### `memory_get`
Retrieve a specific memory by exact key.
- **Parameters**: `key` (required), `scope` (optional)
- **Returns**: Memory value and metadata, or "not found"

### `memory_forget`
Delete a specific memory.
- **Parameters**: `key` (required), `scope` (optional)
- **Returns**: Confirmation or "not found"

### `memory_status`
Check health of the memory backend.
- **Parameters**: None
- **Returns**: Backend status and dependency health

## Scoping Model

All tools accept an optional `scope` parameter:

| Scope | Resolves to user_id | Isolation level |
|-------|---------------------|-----------------|
| `machine` (default) | `cc-{hostname}` | Per-machine |
| `shared` | `cc-shared` | All machines |
| `project` | `cc-proj-{cwd_dirname}` | Per-project directory |

## Transport

- **Protocol**: MCP (Model Context Protocol)
- **Transport**: stdio (stdin/stdout JSON-RPC)
- **Lifecycle**: Spawned per Claude Code session, exits when session ends

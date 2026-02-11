"""MCP server providing persistent semantic memory for Claude Code."""

from mcp.server.fastmcp import FastMCP

from claude_memory_mcp.client import MemoryClient
from claude_memory_mcp.config import settings
from claude_memory_mcp.scoping import resolve_user_id

mcp = FastMCP(
    "claude-memory",
    instructions="Persistent semantic memory for Claude Code sessions",
)

_client = MemoryClient(settings.memory_api_url, settings.memory_api_token)


@mcp.tool()
async def memory_store(
    key: str,
    value: str,
    tags: str = "",
    scope: str = "",
) -> str:
    """Store a memory. Use for session progress, lessons learned, and important context.

    Args:
        key: Descriptive identifier (e.g. "session-2026-02-07-auth-refactor")
        value: The content to remember
        tags: Comma-separated tags for categorization (e.g. "session,progress")
        scope: machine (default), shared (all machines), or project (current project)
    """
    user_id = resolve_user_id(scope or None, settings.memory_default_scope)
    result = await _client.store(
        key=key,
        value=value,
        user_id=user_id,
        tags=tags,
        scope="user",
    )
    return f"Stored memory '{result['key']}' (scope: {user_id})"


@mcp.tool()
async def memory_search(
    query: str,
    limit: int = 5,
    scope: str = "",
) -> str:
    """Search memories semantically. Returns the most relevant matches.

    Args:
        query: Natural language search query
        limit: Max results to return (default 5)
        scope: machine (default), shared (all machines), or project (current project)
    """
    if not query or not query.strip():
        return "No memories found."

    user_id = resolve_user_id(scope or None, settings.memory_default_scope)
    result = await _client.search(
        query=query,
        user_id=user_id,
        limit=limit,
        scope="user",
    )
    if result["status"] != "ok" or not result.get("results"):
        return "No memories found."

    lines = []
    for mem in result["results"]:
        score = f" (score: {mem['score']:.3f})" if mem.get("score") else ""
        tags = f" [{mem['tags']}]" if mem.get("tags") else ""
        lines.append(f"**{mem['key']}**{tags}{score}\n{mem['value']}")
    return "\n\n---\n\n".join(lines)


@mcp.tool()
async def memory_get(
    key: str,
    scope: str = "",
) -> str:
    """Retrieve a specific memory by its exact key.

    Args:
        key: The exact key of the memory to retrieve
        scope: machine (default), shared (all machines), or project (current project)
    """
    user_id = resolve_user_id(scope or None, settings.memory_default_scope)
    result = await _client.get(key=key, user_id=user_id)
    if result["status"] == "not_found":
        return f"No memory found with key '{key}'"
    mem = result["memory"]
    tags = f"\nTags: {mem['tags']}" if mem.get("tags") else ""
    return f"**{mem['key']}**{tags}\n{mem['value']}"


@mcp.tool()
async def memory_forget(
    key: str,
    scope: str = "",
) -> str:
    """Delete a specific memory by its exact key.

    Args:
        key: The exact key of the memory to delete
        scope: machine (default), shared (all machines), or project (current project)
    """
    user_id = resolve_user_id(scope or None, settings.memory_default_scope)
    result = await _client.forget(key=key, user_id=user_id)
    if result["status"] == "not_found":
        return f"No memory found with key '{key}'"
    return f"Deleted memory '{key}'"


@mcp.tool()
async def memory_status() -> str:
    """Check the health of the memory service and show connection status."""
    try:
        result = await _client.health()
        checks = result.get("checks", {})
        status = result.get("status", "unknown")
        lines = [f"Memory service: {status}"]
        for name, ok in checks.items():
            lines.append(f"  {name}: {'ok' if ok else 'FAILED'}")
        return "\n".join(lines)
    except Exception as e:
        return f"Memory service unreachable: {e}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

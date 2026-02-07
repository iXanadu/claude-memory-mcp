import httpx
import respx

from claude_memory_mcp.client import MemoryClient


async def test_store(mock_api):
    mock_api.post("/memory/set").mock(
        return_value=httpx.Response(200, json={"status": "ok", "key": "test-key"})
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.store(
        key="test-key", value="test value", user_id="cc-testhost"
    )
    assert result == {"status": "ok", "key": "test-key"}


async def test_get_found(mock_api):
    mock_api.post("/memory/get").mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "ok",
                "memory": {
                    "key": "test-key",
                    "value": "test value",
                    "scope": "user",
                    "user_id": "cc-testhost",
                    "tags": "test",
                    "tags_search": "",
                },
            },
        )
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.get(key="test-key", user_id="cc-testhost")
    assert result["status"] == "ok"
    assert result["memory"]["value"] == "test value"


async def test_get_not_found(mock_api):
    mock_api.post("/memory/get").mock(
        return_value=httpx.Response(200, json={"status": "not_found", "memory": None})
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.get(key="missing", user_id="cc-testhost")
    assert result["status"] == "not_found"


async def test_search(mock_api):
    mock_api.post("/memory/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "ok",
                "results": [
                    {
                        "key": "color",
                        "value": "blue",
                        "scope": "user",
                        "tags": "pref",
                        "tags_search": "",
                        "score": 0.85,
                    }
                ],
            },
        )
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.search(query="favorite color", user_id="cc-testhost")
    assert result["status"] == "ok"
    assert len(result["results"]) == 1
    assert result["results"][0]["score"] == 0.85


async def test_forget(mock_api):
    mock_api.post("/memory/forget").mock(
        return_value=httpx.Response(200, json={"status": "ok", "key": "test-key"})
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.forget(key="test-key", user_id="cc-testhost")
    assert result["status"] == "ok"


async def test_health(mock_api):
    mock_api.get("/health").mock(
        return_value=httpx.Response(
            200,
            json={"status": "ok", "checks": {"postgres": True, "ollama": True}},
        )
    )
    client = MemoryClient("http://localhost:8920")
    result = await client.health()
    assert result["status"] == "ok"
    assert result["checks"]["postgres"] is True

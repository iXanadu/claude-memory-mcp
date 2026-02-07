import httpx


class MemoryClient:
    """Async HTTP client for the ha-semantic-memory REST API."""

    def __init__(self, base_url: str = "http://localhost:8920", api_token: str = ""):
        self.base_url = base_url.rstrip("/")
        self._headers = {}
        if api_token:
            self._headers["Authorization"] = f"Bearer {api_token}"

    async def store(
        self,
        key: str,
        value: str,
        user_id: str,
        tags: str = "",
        scope: str = "user",
    ) -> dict:
        async with httpx.AsyncClient(headers=self._headers) as client:
            resp = await client.post(
                f"{self.base_url}/memory/set",
                json={
                    "key": key,
                    "value": value,
                    "user_id": user_id,
                    "tags": tags,
                    "scope": scope,
                },
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def get(self, key: str, user_id: str) -> dict:
        async with httpx.AsyncClient(headers=self._headers) as client:
            resp = await client.post(
                f"{self.base_url}/memory/get",
                json={"key": key, "user_id": user_id},
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def search(
        self,
        query: str,
        user_id: str,
        limit: int = 5,
        scope: str = "user",
    ) -> dict:
        async with httpx.AsyncClient(headers=self._headers) as client:
            resp = await client.post(
                f"{self.base_url}/memory/search",
                json={
                    "query": query,
                    "user_id": user_id,
                    "limit": limit,
                    "scope": scope,
                },
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def forget(self, key: str, user_id: str) -> dict:
        async with httpx.AsyncClient(headers=self._headers) as client:
            resp = await client.post(
                f"{self.base_url}/memory/forget",
                json={"key": key, "user_id": user_id},
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(headers=self._headers) as client:
            resp = await client.get(
                f"{self.base_url}/health",
                timeout=10.0,
            )
            resp.raise_for_status()
            return resp.json()

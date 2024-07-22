from httpx import AsyncClient


async def mock_http_client(app, base_url, path, token=None):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        if token:
            ac.headers["Authorization"] = token
        return await ac.get(path)


async def mock_http_post_client(app, base_url, path, payload):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        return await ac.post(path, json=payload)

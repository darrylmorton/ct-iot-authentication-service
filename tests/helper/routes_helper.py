from httpx import AsyncClient, ASGITransport, Response

from tests.config import APP_PORT


class RoutesHelper:
    TEST_URL = f"http://localhost:{APP_PORT}"

    @staticmethod
    async def http_client(app, base_url, path, token=None) -> Response:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=base_url
        ) as ac:
            if token:
                ac.headers["Authorization"] = token

            return await ac.get(path)

    @staticmethod
    async def http_post_client(app, base_url, path, payload) -> Response:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=base_url
        ) as ac:
            return await ac.post(path, json=payload)

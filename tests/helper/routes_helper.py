from httpx import AsyncClient, ASGITransport, Response

from tests.config import APP_PORT


class RoutesHelper:
    TEST_URL = f"http://localhost:{APP_PORT}"

    @staticmethod
    async def http_client(app, path, token=None) -> Response:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=RoutesHelper.TEST_URL
        ) as ac:
            if token:
                ac.headers["auth-token"] = token

            return await ac.get(path)

    @staticmethod
    async def http_post_client(app, path, payload) -> Response:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=RoutesHelper.TEST_URL
        ) as ac:
            return await ac.post(path, json=payload)

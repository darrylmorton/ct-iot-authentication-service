from authentication_service.service import server
from config import APP_VERSION
from tests.helper.routes_helper import RoutesHelper


class TestHealth:
    async def test_health(self):
        expected_result = {"message": "ok", "version": APP_VERSION}

        response = await RoutesHelper.http_client(
            server, RoutesHelper.TEST_URL, "/healthz"
        )

        assert response.status_code == 200
        assert response.json() == expected_result

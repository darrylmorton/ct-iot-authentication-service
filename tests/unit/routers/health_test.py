from authentication_service.service import server
from config import APP_VERSION
from tests.helper.routes_helper import mock_http_client


class TestHealth:
    async def test_health(self):
        response = await mock_http_client(server, "http://test", "healthz")

        assert response.status_code == 200
        assert response.json() == {"message": "ok", "version": APP_VERSION}

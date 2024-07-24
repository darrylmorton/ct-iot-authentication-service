from jose import jwt

from authentication_service.service import server
from config import JWT_SECRET
from tests.helper.jwt_helper import create_token_expiry
from tests.helper.routes_helper import mock_http_client


class TestJwtVerify:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    token = jwt.encode(
        {"id": id, "exp": create_token_expiry()},
        JWT_SECRET,
        algorithm="HS256",
    )

    async def test_valid_token(self):
        response = await mock_http_client(server, "http://test", "api/jwt", self.token)
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result["id"] == self.id

    async def test_missing_token(self):
        response = await mock_http_client(server, "http://test", "api/jwt", {})

        assert response.status_code == 401

    async def test_expired_token(self):
        expired_token = jwt.encode(
            {"id": self.id, "exp": create_token_expiry(-1)},
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await mock_http_client(
            server, "http://test", "api/jwt", expired_token
        )

        assert response.status_code == 401

    async def test_invalid_token_id(self):
        invalid_token = jwt.encode(
            {
                "id": "1b7f4d5a-161d-4b3a-8b33",
                "exp": create_token_expiry(),
            },
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await mock_http_client(
            server, "http://test", "api/jwt", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_missing_id(self):
        invalid_token = jwt.encode(
            {"exp": create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await mock_http_client(
            server, "http://test", "api/jwt", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_secret(self):
        invalid_token = jwt.encode(
            {"id": self.id, "exp": create_token_expiry()},
            "",
            algorithm="HS256",
        )
        response = await mock_http_client(
            server, "http://test", "api/jwt", invalid_token
        )

        assert response.status_code == 401

from jose import jwt

from authentication_service.service import server
from config import JWT_SECRET
from tests.helper.jwt_helper import create_token_expiry
from tests.helper.routes_helper import mock_http_client


class TestJwtVerify:
    username = "foo@home.com"
    token = jwt.encode(
        {"username": username, "exp": create_token_expiry()},
        JWT_SECRET,
        algorithm="HS256",
    )

    async def test_valid_token(self):
        response = await mock_http_client(server, "http://test", "api/jwt", self.token)
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result["username"] == self.username

    async def test_missing_token(self):
        response = await mock_http_client(server, "http://test", "api/jwt", {})

        assert response.status_code == 401

    async def test_expired_token(self):
        expired_token = jwt.encode(
            {"username": self.username, "exp": create_token_expiry(-1)},
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await mock_http_client(
            server, "http://test", "api/jwt", expired_token
        )

        assert response.status_code == 401

    async def test_invalid_token_username_str(self):
        invalid_token = jwt.encode(
            {"username": "foo", "exp": create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await mock_http_client(
            server, "http://test", "api/jwt", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_missing_username(self):
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
            {"username": self.username, "exp": create_token_expiry()},
            "",
            algorithm="HS256",
        )
        response = await mock_http_client(
            server, "http://test", "api/jwt", invalid_token
        )

        assert response.status_code == 401

from jose import jwt

from authentication_service.service import server
from config import JWT_SECRET
from tests.helper.jwt_helper import create_token_expiry
from tests.helper.routes_helper import mock_http_post_client


class TestJwt:
    username = "foo@home.com"
    token = jwt.encode(
        {"username": username, "exp": create_token_expiry()},
        JWT_SECRET,
        algorithm="HS256",
    )

    async def test_post_jwt_missing_username(self):
        payload = {}

        response = await mock_http_post_client(
            server, "http://test", "api/jwt", payload
        )

        assert response.status_code == 401

    async def test_post_jwt_invalid_username(self):
        payload = {"username": "foo"}

        response = await mock_http_post_client(
            server, "http://test", "api/jwt", payload
        )

        assert response.status_code == 401

    async def test_post_jwt_success(self):
        payload = {"username": self.username}

        response = await mock_http_post_client(
            server, "http://test", "api/jwt", payload
        )
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 201
        assert actual_result["username"] == self.username

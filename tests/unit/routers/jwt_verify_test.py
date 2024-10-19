from jose import jwt

from authentication_service.service import app
from config import JWT_SECRET
from tests.helper.jwt_helper import JwtHelper
from tests.helper.routes_helper import RoutesHelper


class TestJwtVerify:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    admin = False
    token = jwt.encode(
        {"id": id, "is_admin": admin, "exp": JwtHelper.create_token_expiry()},
        JWT_SECRET,
        algorithm="HS256",
    )

    async def test_valid_token(self):
        response = await RoutesHelper.http_client(app, "/api/jwt", self.token)
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result["id"] == self.id
        assert actual_result["admin"] == self.admin

    async def test_missing_token(self):
        response = await RoutesHelper.http_client(app, "/api/jwt", {})

        assert response.status_code == 401

    async def test_expired_token(self):
        expired_token = jwt.encode(
            {
                "id": self.id,
                "is_admin": self.admin,
                "exp": JwtHelper.create_token_expiry(-1),
            },
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await RoutesHelper.http_client(app, "/api/jwt", expired_token)

        assert response.status_code == 401

    async def test_invalid_token_id(self):
        invalid_token = jwt.encode(
            {
                "id": "1b7f4d5a-161d-4b3a-8b33",
                "is_admin": self.admin,
                "exp": JwtHelper.create_token_expiry(),
            },
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(app, "/api/jwt", invalid_token)

        assert response.status_code == 401

    async def test_invalid_token_missing_id(self):
        invalid_token = jwt.encode(
            {"is_admin": self.admin, "exp": JwtHelper.create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(app, "/api/jwt", invalid_token)

        assert response.status_code == 401

    async def test_invalid_token_missing_is_admin(self):
        invalid_token = jwt.encode(
            {"id": self.id, "exp": JwtHelper.create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(app, "/api/jwt", invalid_token)

        assert response.status_code == 401

    async def test_invalid_token_secret(self):
        invalid_token = jwt.encode(
            {
                "id": self.id,
                "is_admin": self.admin,
                "exp": JwtHelper.create_token_expiry(),
            },
            "",
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(app, "/api/jwt", invalid_token)

        assert response.status_code == 401

from jose import jwt

from authentication_service.service import app
import tests.config as test_config
from tests.helper.routes_helper import RoutesHelper
from utils.auth_util import AuthUtil


class TestJwtCreateAuthentication:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    is_admin = False
    token = jwt.encode(
        {"id": id, "is_admin": is_admin, "exp": AuthUtil.create_token_expiry()},
        test_config.JWT_SECRET,
        algorithm="HS256",
    )

    async def test_post_jwt_missing_id(self):
        payload = {"is_admin": self.is_admin}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)

        assert response.status_code == 401

    async def test_post_jwt_invalid_id(self):
        payload = {"id": "1b7f4d5a-161d-4b3a-8b33", "is_admin": self.is_admin}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)

        assert response.status_code == 401

    async def test_post_jwt_missing_admin(self):
        payload = {"id": self.id}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)

        assert response.status_code == 401

    async def test_post_jwt_invalid_admin(self):
        payload = {"id": self.id, "is_admin": "abc"}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)

        assert response.status_code == 401

    async def test_post_jwt_success(self):
        payload = {"id": self.id, "is_admin": self.is_admin}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], test_config.JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["id"] == self.id
        assert actual_result["is_admin"] == self.is_admin

    async def test_post_jwt_success_with_admin(self):
        payload = {"id": self.id, "is_admin": self.is_admin}

        response = await RoutesHelper.http_post_client(app, "/api/jwt", payload)
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], test_config.JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["id"] == self.id
        assert actual_result["is_admin"] == self.is_admin

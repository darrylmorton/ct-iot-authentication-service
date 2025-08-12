from jose import jwt

from authentication_service.service import app
import tests.config as test_config
from tests.helper.routes_helper import RoutesHelper
from utils.confirm_account_util import ConfirmAccountUtil


class TestJwtCreateConfirmAccount:
    username = "foo@example.com"
    email_type = test_config.EMAIL_VERIFICATION_TYPES[0]
    token = jwt.encode(
        {
            "username": username,
            "email_type": email_type,
            "exp": ConfirmAccountUtil.create_token_expiry(),
        },
        test_config.JWT_SECRET_CONFIRM_ACCOUNT,
        algorithm="HS256",
    )

    async def test_post_missing_username(self):
        payload = {"email_type": self.email_type}

        response = await RoutesHelper.http_post_client(
            app, "/api/jwt/confirm-account", payload
        )

        assert response.status_code == 401

    async def test_post_invalid_username(self):
        payload = {"username": "example.com", "email_type": self.email_type}

        response = await RoutesHelper.http_post_client(
            app, "/api/jwt/confirm-account", payload
        )

        assert response.status_code == 401

    async def test_post_missing_email_type(self):
        payload = {"username": self.username}

        response = await RoutesHelper.http_post_client(
            app, "/api/jwt/confirm-account", payload
        )

        assert response.status_code == 401

    async def test_post_invalid_email_type(self):
        payload = {"username": self.username, "email_type": "EMAIL_TYPE_INVALID"}

        response = await RoutesHelper.http_post_client(
            app, "/api/jwt/confirm-account", payload
        )

        assert response.status_code == 401

    async def test_post_success(self):
        payload = {"username": self.username, "email_type": self.email_type}

        response = await RoutesHelper.http_post_client(
            app, "/api/jwt/confirm-account", payload
        )
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"],
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithms=["HS256"],
        )

        assert response.status_code == 200
        assert actual_result["username"] == self.username
        assert actual_result["email_type"] == self.email_type

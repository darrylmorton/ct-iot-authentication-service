from jose import jwt

import config
import tests.config as test_config
from authentication_service.service import app
from tests.helper.routes_helper import RoutesHelper
from utils.confirm_account_util import ConfirmAccountUtil


class TestJwtVerifyConfirmAccount:
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

    async def test_valid_token(self):
        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", self.token
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result["username"] == self.username
        assert actual_result["email_type"] == self.email_type

    async def test_missing_token(self):
        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", {}
        )

        assert response.status_code == 401

    async def test_expired_token(self):
        expired_token = jwt.encode(
            {
                "username": self.username,
                "email_type": self.email_type,
                "exp": ConfirmAccountUtil.create_token_expiry(-1),
            },
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithm="HS256",
        )

        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", expired_token
        )

        assert response.status_code == config.HTTP_STATUS_CODE_EXPIRED_TOKEN

    async def test_invalid_token_username(self):
        invalid_token = jwt.encode(
            {
                "username": "example.com",
                "email_type": self.email_type,
                "exp": ConfirmAccountUtil.create_token_expiry(),
            },
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithm="HS256",
        )

        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_missing_username(self):
        invalid_token = jwt.encode(
            {
                "email_type": self.email_type,
                "exp": ConfirmAccountUtil.create_token_expiry(),
            },
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_missing_email_type(self):
        invalid_token = jwt.encode(
            {
                "username": self.username,
                "exp": ConfirmAccountUtil.create_token_expiry(),
            },
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", invalid_token
        )

        assert response.status_code == 401

    async def test_invalid_token_secret(self):
        invalid_token = jwt.encode(
            {
                "username": self.username,
                "email_type": self.email_type,
                "exp": ConfirmAccountUtil.create_token_expiry(),
            },
            "",
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(
            app, "/api/jwt/confirm-account", "confirm-account-token", invalid_token
        )

        assert response.status_code == 401

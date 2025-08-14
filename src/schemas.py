from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from email_validator import EmailSyntaxError, validate_email
from fastapi import HTTPException
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    ConfigDict,
)
from pydantic.types import UuidVersion
from pydantic_core.core_schema import ValidationInfo

import config
from decorators.metrics import REQUEST_COUNT
from utils.app_util import AppUtil
from utils.auth_util import AuthUtil
from utils.confirm_account_util import ConfirmAccountUtil


# TODO validate missing fields in JWT payload
class JwtPayloadBase(BaseModel):
    id: UUID = Annotated[UUID, UuidVersion(4)]
    is_admin: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"id": "848a3cdd-cafd-4ec6-a921-afb0bcc841dd", "is_admin": False},
                {"id": "eaf0bb67-288b-4e56-860d-e727b4f57ff9", "is_admin": True},
            ]
        },
    )


class JwtPayload(JwtPayloadBase):
    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if not AppUtil.validate_uuid4(v):
            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.UNAUTHORIZED,
                path="/jwt/authentication",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT {info.field_name} is not a valid UUID4",
            )

        return v

    @field_validator("is_admin", mode="before")
    @classmethod
    def validate_is_admin(cls, v: str, info: ValidationInfo):
        if not isinstance(v, bool):
            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.UNAUTHORIZED,
                path="/jwt/authentication",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT {info.field_name} is not a boolean",
            )

        return v


class JwtVerifyBase(BaseModel):
    auth_token: str = Field(alias="auth-token", validation_alias="auth_token")

    model_config = ConfigDict(from_attributes=True)


class JwtVerify(JwtVerifyBase):
    @field_validator("auth_token", mode="before")
    @classmethod
    def validate_auth_token_header(cls, v: str):
        payload = {}

        try:
            payload = AuthUtil.decode_token(token=v)
            JwtPayload.model_validate(payload)

        except KeyError:
            REQUEST_COUNT.labels(
                method="GET", status=HTTPStatus.UNAUTHORIZED, path="/jwt/authentication"
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT payload {payload}",
            )

        return v


class ConfirmAccountPayloadBase(BaseModel):
    username: str
    email_type: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "foo@example.com",
                    "email_type": config.EMAIL_VERIFICATION_TYPES[0],
                },
            ]
        },
    )


class ConfirmAccountPayload(ConfirmAccountPayloadBase):
    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        try:
            validate_email(v, check_deliverability=False)

        except EmailSyntaxError:
            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.UNAUTHORIZED,
                path="/jwt/confirm-account",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT {info.field_name} is not an email",
            )

        return v

    @field_validator("email_type", mode="before")
    @classmethod
    def validate_email_type(cls, v: str, info: ValidationInfo):
        if not AppUtil.email_types(v):
            REQUEST_COUNT.labels(
                method="POST",
                status=HTTPStatus.UNAUTHORIZED,
                path="/jwt/confirm-account",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT {info.field_name} is not an email type",
            )

        return v


class ConfirmAccountHeaderBase(BaseModel):
    confirm_account_token: str = Field(
        alias="confirm-account-token", validation_alias="confirm_account_token"
    )

    model_config = ConfigDict(from_attributes=True)


class ConfirmAccountHeader(ConfirmAccountHeaderBase):
    @field_validator("confirm_account_token", mode="before")
    @classmethod
    def validate_confirm_account_token_header(cls, v: str):
        payload = {}

        try:
            payload = ConfirmAccountUtil.decode_token(token=v)
            ConfirmAccountPayload.model_validate(payload)

        except KeyError:
            REQUEST_COUNT.labels(
                method="GET",
                status=HTTPStatus.UNAUTHORIZED,
                path="/jwt/confirm-account",
            ).inc()

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid JWT payload {payload}",
            )

        return v

from http import HTTPStatus

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    ConfigDict,
)
from pydantic_core.core_schema import ValidationInfo

from decorators.metrics import REQUEST_COUNT
from utils.app_util import AppUtil
from utils.auth_util import AuthUtil


# TODO validate missing fields in JWT payload
class JwtBase(BaseModel):
    id: str
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


class JwtPayload(JwtBase):
    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if not AppUtil.validate_uuid4(v):
            try:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail=f"Invalid JWT {info.field_name} is not a valid UUID4",
                )
            finally:
                REQUEST_COUNT.labels(
                    method="POST", status=HTTPStatus.UNAUTHORIZED, path="/jwt"
                ).inc()

        return v

    @field_validator("is_admin", mode="before")
    @classmethod
    def validate_is_admin(cls, v: str, info: ValidationInfo):
        if not isinstance(v, bool):
            try:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail=f"Invalid JWT {info.field_name} is not a boolean",
                )
            finally:
                REQUEST_COUNT.labels(
                    method="POST", status=HTTPStatus.UNAUTHORIZED, path="/jwt"
                ).inc()

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
            payload = AuthUtil.decode_token(auth_token=v)
            JwtPayload.model_validate(payload)

        except KeyError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"fInvalid JWT payload {payload}",
            )

        return v

from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, Field, ConfigDict
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil
from utils.auth_util import AuthUtil


class JwtBase(BaseModel):
    id: str

    model_config = ConfigDict(from_attributes=True)


class Jwt(JwtBase):
    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT id"
            )

        return v


class JwtIsAdminBase(Jwt):
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


class JwtPayload(JwtIsAdminBase):
    @field_validator("is_admin")
    @classmethod
    def validate_is_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "is_admin" and not isinstance(v, bool):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT is_admin"
            )

        return v


class JwtVerifyBase(BaseModel):
    auth_token: str = Field(alias="auth-token", validation_alias="auth_token")

    model_config = ConfigDict(from_attributes=True)


class JwtVerify(JwtVerifyBase):
    @field_validator("auth_token")
    @classmethod
    def validate_auth_token_header(cls, v: str, info: ValidationInfo):
        if info.field_name == "auth_token" and not isinstance(v, str):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid request header"
            )

        try:
            payload = AuthUtil.decode_token(v)

            JwtPayload.model_validate(payload)
        except KeyError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT payload"
            )

        return v

from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil
from utils.auth_util import AuthUtil


class JwtBase(BaseModel):
    id: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            raise HTTPException(status_code=401, detail="Invalid JWT id")

        return v


class JwtCreateBase(JwtBase):
    admin: bool

    @field_validator("admin")
    @classmethod
    def validate_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "admin" and not isinstance(v, bool):
            raise HTTPException(status_code=401, detail="Invalid JWT is_admin")

        return v


class JwtCreate(JwtCreateBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": "848a3cdd-cafd-4ec6-a921-afb0bcc841dd", "admin": False},
                {"id": "eaf0bb67-288b-4e56-860d-e727b4f57ff9", "admin": True},
            ]
        }
    }

    class ConfigDict:
        from_attributes = True


class JwtPayloadBase(JwtBase):
    is_admin: bool

    @field_validator("is_admin")
    @classmethod
    def validate_is_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "is_admin" and not isinstance(v, bool):
            raise HTTPException(status_code=401, detail="Invalid JWT is_admin")

        return v


class JwtPayload(JwtPayloadBase):
    class ConfigDict:
        from_attributes = True


class JwtVerifyBase(BaseModel):
    auth_token: str = Field(alias="auth-token", validation_alias="auth_token")

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


class JwtVerify(JwtVerifyBase):
    class ConfigDict:
        from_attributes = True

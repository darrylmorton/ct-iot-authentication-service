from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil

from logger import log
from utils.auth_util import AuthUtil


class JwtBase(BaseModel):
    id: str


class JwtCreateBase(JwtBase):
    admin: bool


class JwtCreate(JwtCreateBase):
    @field_validator("id")  # , mode="before", check_fields=True)
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        log.info(f"validate_id: {v=}")
        log.info(f"validate_id: {info=}")

        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            raise HTTPException(status_code=401, detail="Invalid JWT id")

        return v

    @field_validator("admin")  # , mode="before", check_fields=True)
    @classmethod
    def validate_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "admin" and not isinstance(v, bool):
            raise HTTPException(status_code=401, detail="Invalid JWT is_admin")

        return v

    class ConfigDict:
        from_attributes = True


class JwtPayloadBase(JwtBase):
    is_admin: bool
    expiry: Optional[int] = None
    exp: Optional[int] = None


class JwtPayload(JwtPayloadBase):
    @field_validator("id")  # , mode="before", check_fields=True)
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            raise HTTPException(status_code=401, detail="Invalid JWT id")

        return v

    @field_validator("is_admin")  # , mode="before", check_fields=True)
    @classmethod
    def validate_is_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "is_admin" and not isinstance(v, bool):
            raise HTTPException(status_code=401, detail="Invalid JWT is_admin")

        return v

    class ConfigDict:
        from_attributes = True


class JwtVerifyBase(BaseModel):
    auth_token: str = Field(alias="auth-token", validation_alias="auth_token")


class JwtVerify(JwtVerifyBase):
    @field_validator("auth_token")  # , mode="before", check_fields=True)
    @classmethod
    def validate_auth_token_header(cls, v: str, info: ValidationInfo):
        log.info(f"validate_auth_token_header: {v=}")
        log.info(f"validate_auth_token_header: {info=}")

        if info.field_name == "auth_token" and not isinstance(v, str):
            log.info(f"validate_auth_token_header FAIL")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid request header"
            )

        try:
            payload = AuthUtil.decode_token(v)
            log.info(f"**** **** validate_auth_token_header {payload=}")

            JwtPayload.model_validate(payload)

            log.info(f"**** validate_auth_token_header {payload=}")

        except KeyError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT payload"
            )

        log.info(f"validate_auth_token_header SUCCESS")

        return v

    class ConfigDict:
        from_attributes = True

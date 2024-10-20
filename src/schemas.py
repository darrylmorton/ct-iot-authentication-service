from typing import Any, Mapping

from fastapi import Header
from pydantic import BaseModel, field_validator, ValidationError, Field
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil

from logger import log


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
            raise ValidationError

        return v

    @field_validator("admin")  # , mode="before", check_fields=True)
    @classmethod
    def validate_admin(cls, v: bool, info: ValidationInfo):
        if info.field_name == "admin" and not isinstance(v, bool):
            raise ValidationError

        return v

    class ConfigDict:
        from_attributes = True


# class JwtVerifyBase(JwtBase):
#     is_admin: bool
#
#
# class JwtVerify(JwtVerifyBase):
#     @field_validator("id")  # , mode="before", check_fields=True)
#     @classmethod
#     def validate_id(cls, v: str, info: ValidationInfo):
#         if info.field_name == "id" and not AppUtil.validate_uuid4(v):
#             raise ValidationError
#
#         return v
#
#     @field_validator("is_admin")  # , mode="before", check_fields=True)
#     @classmethod
#     def validate_admin(cls, v: bool, info: ValidationInfo):
#         if info.field_name == "iss_admin" and not isinstance(v, bool):
#             raise ValidationError
#
#         return v
#
#     class ConfigDict:
#         from_attributes = True


class JwtVerifyBase(BaseModel):
    authorization: str | None


class JwtVerify(JwtVerifyBase):
    @field_validator("authorization") # , mode="before", check_fields=True)
    @classmethod
    def validate_authorization(cls, v: str, info: ValidationInfo):
        log.info(f"validate_authorization: {v=}")
        log.info(f"validate_authorization: {info=}")
        # if info.field_name == "id" and not AppUtil.validate_uuid4(v):
        #     raise ValidationError

        return v

    # @field_validator("is_admin")  # , mode="before", check_fields=True)
    # @classmethod
    # def validate_admin(cls, v: bool, info: ValidationInfo):
    #     if info.field_name == "iss_admin" and not isinstance(v, bool):
    #         raise ValidationError
    #
    #     return v

    class ConfigDict:
        from_attributes = False

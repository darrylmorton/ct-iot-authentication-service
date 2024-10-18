from pydantic import BaseModel, field_validator, ValidationError
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil


class JwtVerifyBase(BaseModel):
    id: str
    admin: bool


class JwtVerify(JwtVerifyBase):
    @field_validator("id", mode="before", check_fields=True)
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        if info.field_name == "id" and not AppUtil.validate_uuid4(v):
            raise ValidationError

        return v

    @field_validator("admin", mode="before", check_fields=True)
    @classmethod
    def validate_admin(cls, v: str, info: ValidationInfo):
        if info.field_name == "admin" and not isinstance(v, bool):
            raise ValidationError

        return v

    class ConfigDict:
        from_attributes = True

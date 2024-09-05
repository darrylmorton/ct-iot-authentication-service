from uuid import UUID

from pydantic import BaseModel


class JwtVerifyBase(BaseModel):
    id: UUID
    admin: bool


class JwtVerify(JwtVerifyBase):
    class ConfigDict:
        from_attributes = True

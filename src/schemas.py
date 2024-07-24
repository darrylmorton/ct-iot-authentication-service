from uuid import UUID

from pydantic import BaseModel


class JwtVerifyBase(BaseModel):
    id: UUID


class JwtVerify(JwtVerifyBase):
    class ConfigDict:
        from_attributes = True

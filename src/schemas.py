from pydantic import BaseModel


class JwtVerifyBase(BaseModel):
    id: str
    is_admin: bool


class JwtVerify(JwtVerifyBase):
    class ConfigDict:
        from_attributes = True

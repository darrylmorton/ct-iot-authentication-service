from pydantic import BaseModel, EmailStr


class JwtVerifyBase(BaseModel):
    username: EmailStr


class JwtVerify(JwtVerifyBase):
    class ConfigDict:
        from_attributes = True

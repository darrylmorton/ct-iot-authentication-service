import datetime
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

import config
from logger import log


class AuthUtil:
    @staticmethod
    def create_token_expiry() -> datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=config.JWT_EXPIRY_SECONDS
        )

    @staticmethod
    def decode_token(auth_token: str) -> dict:
        try:
            return jwt.decode(auth_token, config.JWT_SECRET, algorithms=["HS256"])

        except TypeError as error:
            log.debug(f"decode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        except ExpiredSignatureError as error:
            log.debug(f"decode_token - expired signature {error}")

            raise HTTPException(
                status_code=config.HTTP_STATUS_CODE_EXPIRED_TOKEN,
                detail="Expired token error",
            )
        except JWTError as error:
            log.debug(f"decode_token - invalid token {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT"
            )
        except KeyError as error:
            log.debug(f"decode_token - invalid key {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT payload"
            )

    @staticmethod
    def encode_token(_id: str, _admin: bool):
        try:
            return {
                "token": jwt.encode(
                    {
                        "id": _id,
                        "is_admin": _admin,
                        "exp": AuthUtil.create_token_expiry(),
                    },
                    config.JWT_SECRET,
                    algorithm="HS256",
                )
            }

        except KeyError as error:
            log.debug(f"encode_token - key error {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        except TypeError as error:
            log.debug(f"encode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        except JWTError as error:
            log.debug(f"encode_token - jwt error {error}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error
            )

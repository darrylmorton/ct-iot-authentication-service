import datetime
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

import config
from config import JWT_TOKEN_EXPIRY_SECONDS
from logger import log


class AuthUtil:
    @staticmethod
    def create_token_expiry() -> datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=JWT_TOKEN_EXPIRY_SECONDS
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])

        except TypeError as error:
            log.debug(f"decode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        except ExpiredSignatureError as error:
            log.debug(f"decode_token - expired signature {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Expired token error"
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

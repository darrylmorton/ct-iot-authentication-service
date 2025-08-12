import datetime
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

import config
from logger import log
from utils.app_util import AppUtil


class ConfirmAccountUtil:
    @staticmethod
    def create_token_expiry(
        _seconds=config.JWT_EXPIRY_SECONDS_CONFIRM_ACCOUNT,
    ) -> datetime:
        return AppUtil.create_token_expiry(int(f"{_seconds}"))

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, config.JWT_SECRET_CONFIRM_ACCOUNT, algorithms=["HS256"]
            )

        except TypeError as error:
            log.debug(f"decode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token error"
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
    def email_type_selector(email_type: str) -> str:
        if AppUtil.email_types(email_type):
            return email_type

        else:
            log.debug(f"email_type_selector - type not found {email_type}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email type not supported",
            )

    @staticmethod
    def encode_token(username: str, email_type: str):
        try:
            return {
                "token": jwt.encode(
                    {
                        "username": username,
                        "email_type": email_type,
                        "exp": ConfirmAccountUtil.create_token_expiry(),
                    },
                    config.JWT_SECRET_CONFIRM_ACCOUNT,
                    algorithm="HS256",
                )
            }
        except KeyError as error:
            log.debug(f"encode_token - key error {error}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token error"
            )
        except TypeError as error:
            log.debug(f"encode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token error"
            )
        except JWTError as error:
            log.debug(f"encode_token - jwt error {error}")

            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)

import datetime
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

import config
from decorators.metrics import REQUEST_COUNT
from logger import log
from utils.app_util import AppUtil


class AuthUtil:
    @staticmethod
    def create_token_expiry(
        _seconds=config.JWT_AUTHENTICATION_EXPIRY_SECONDS,
    ) -> datetime:
        return AppUtil.create_token_expiry(int(f"{_seconds}"))

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(
                token, config.JWT_AUTHENTICATION_SECRET, algorithms=["HS256"]
            )

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
        finally:
            REQUEST_COUNT.labels(
                method="GET", status=HTTPStatus.UNAUTHORIZED, path="/jwt/authentication"
            ).inc()

    @staticmethod
    def encode_token(_id: str, _admin: bool, route_path: str, method: str):
        try:
            return {
                "token": jwt.encode(
                    {
                        "id": _id,
                        "is_admin": _admin,
                        "exp": AuthUtil.create_token_expiry(),
                    },
                    config.JWT_AUTHENTICATION_SECRET,
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

            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=error)
        finally:
            REQUEST_COUNT.labels(
                method=method, status=HTTPStatus.UNAUTHORIZED, path=route_path
            ).inc()

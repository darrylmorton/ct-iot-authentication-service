from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from jose import jwt, ExpiredSignatureError, JWTError
from pydantic_core import ValidationError

from starlette.requests import Request, Headers
from starlette.responses import JSONResponse

import config
import schemas
from schemas import JwtVerify
from utils.auth_util import AuthUtil

from logger import log

router = APIRouter()


@router.post("/jwt", status_code=HTTPStatus.CREATED)
async def jwt_create(payload: schemas.JwtCreate) -> JSONResponse:
    try:
        token = {
            "token": jwt.encode(
                {
                    "id": payload.id,
                    "is_admin": payload.admin,
                    "exp": AuthUtil.create_token_expiry(),
                },
                config.JWT_SECRET,
                algorithm="HS256",
            )
        }

        return JSONResponse(status_code=HTTPStatus.CREATED, content=token)
    # except ValidationError as error:
    #     log.debug(f"jwt_create - validation error {error}")
    #
    #     return JSONResponse(
    #         status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
    #     )
    except KeyError as error:
        log.debug(f"jwt_create - key error {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except TypeError as error:
        log.debug(f"jwt_create - type error {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except JWTError as error:
        log.debug(f"jwt_create - jwt error {error}")

        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error)


@router.get("/jwt", status_code=HTTPStatus.OK)
# async def jwt_verify(authorization: str | None = Header(default=None)) -> JSONResponse:
async def jwt_verify(headers: schemas.JwtVerify) -> JSONResponse:
    log.info(f"**** jwt_verify {headers=}")

    try:
        # auth_token = req.headers["Authorization"]

        if not headers:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        payload = jwt.decode(
            headers, config.JWT_SECRET, algorithms=["HS256"]
        )

        # schemas.JwtVerify.model_validate(payload)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"id": payload["id"], "admin": payload["is_admin"]},
        )
    except KeyError as error:
        log.debug(f"jwt_verify - invalid key {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid key error"
        )
    except TypeError as error:
        log.debug(f"jwt_verify - type error {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except ExpiredSignatureError as error:
        log.debug(f"jwt_verify - expired signature {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Expired token error"
        )
    except JWTError as error:
        log.debug(f"jwt_verify - invalid token {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid token error"
        )
    except ValidationError as error:
        log.debug(f"jwt_verify - invalid token {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid token error"
        )

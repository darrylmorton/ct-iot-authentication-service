from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from pydantic_core import ValidationError

from starlette.requests import Request
from starlette.responses import JSONResponse

import config
from tests.schemas import JwtVerify
from utils import auth_util

from logger import log

router = APIRouter()


@router.post("/jwt", status_code=HTTPStatus.CREATED)
async def create_jwt(req: Request) -> JSONResponse:
    try:
        payload = await req.json()

        JwtVerify.model_validate(payload)

        token = {
            "token": jwt.encode(
                {
                    "username": payload["username"],
                    "exp": auth_util.create_token_expiry(),
                },
                config.JWT_SECRET,
                algorithm="HS256",
            )
        }

        return JSONResponse(status_code=HTTPStatus.CREATED, content=token)
    except ValidationError as error:
        log.debug(f"jwt create {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except KeyError as error:
        log.debug(f"jwt create {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
        )
    except TypeError as error:
        log.debug(f"jwt create {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="*** Unauthorised error"
        )
    except JWTError as error:
        log.debug(f"jwt create {error}")

        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error)


@router.get("/jwt/verify", status_code=HTTPStatus.OK)
async def jwt_verify(req: Request) -> JSONResponse:
    auth_token = req.headers["Authorization"]

    if not auth_token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    try:
        payload = jwt.decode(auth_token, config.JWT_SECRET, algorithms=["HS256"])

        JwtVerify.model_validate(payload)

        # if username:
        return JSONResponse(status_code=HTTPStatus.OK, content="Success")
        # else:
        #     raise HTTPException(
        #         status_code=HTTPStatus.UNAUTHORIZED, detail="invalid jwt"
        #     )
    except KeyError as error:
        log.debug(f"verify_jwt - invalid key {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid key error"
        )
    except ExpiredSignatureError as error:
        log.debug(f"verify_jwt - expired signature {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Expired token error"
        )
    except JWTError as error:
        log.debug(f"verify_jwt - invalid token {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid token error"
        )
    except TypeError as error:
        log.debug(f"verify_jwt - invalid username {error}")

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED, content="Invalid token error"
        )

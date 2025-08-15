from http import HTTPStatus

from fastapi import APIRouter, Header, Body, HTTPException
from starlette.responses import JSONResponse

import schemas
from decorators.metrics import observability
from logger import log
from utils.auth_util import AuthUtil

router = APIRouter()

ROUTE_PATH = "/jwt/authentication"


@router.post(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method="POST")
async def jwt_create_authentication_token(
    payload: schemas.JwtPayload = Body(embed=False),
) -> JSONResponse:
    log.info(f"*** jwt_create_authentication_token {payload=}")

    try:
        token = AuthUtil.encode_token(
            _id=payload.id,
            _admin=payload.is_admin,
            route_path=ROUTE_PATH,
            method="POST",
        )
        log.info(f"*** jwt_create_authentication_token {token=}")

        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as error:
        log.error(f"jwt_create_authentication_token error {error}")

        return JSONResponse(
            status_code=error.status_code, content={"message": "jwt create error"}
        )
    except Exception as error:
        log.error(f"jwt_create_authentication_token server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt create server error"},
        )


@router.get(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method="GET")
async def jwt_verify_authentication_token(
    headers: schemas.JwtVerify = Header(
        alias="auth-token", validation_alias="auth_token", convert_underscores=True
    ),
) -> JSONResponse:
    try:
        payload = AuthUtil.decode_token(token=headers.auth_token)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "id": payload["id"],
                "is_admin": payload["is_admin"],
            },
        )
    except HTTPException as error:
        log.error(f"jwt_verify_authentication_token error {error}")

        return JSONResponse(
            status_code=error.status_code, content={"message": "jwt verify error"}
        )
    except Exception as error:
        log.error(f"jwt_verify_authentication_token server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt verify server error"},
        )

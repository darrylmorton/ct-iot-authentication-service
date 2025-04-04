from http import HTTPStatus

from fastapi import APIRouter, Header, Body, HTTPException
from starlette.responses import JSONResponse

import schemas
from logger import log
from utils.auth_util import AuthUtil

router = APIRouter()

ROUTER_PATH = "/jwt"


@router.post(ROUTER_PATH, status_code=HTTPStatus.OK)
async def jwt_create(
    payload: schemas.JwtPayload = Body(embed=False),
) -> JSONResponse:
    try:
        token = AuthUtil.encode_token(_id=payload.id, _admin=payload.is_admin)

        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as error:
        log.error(f"jwt create error {error}")

        return JSONResponse(
            status_code=error.status_code, content={"message": "jwt create error"}
        )
    except Exception as error:
        log.error(f"jwt verify server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt verify server error"},
        )


@router.get(ROUTER_PATH, status_code=HTTPStatus.OK)
async def jwt_verify(
    headers: schemas.JwtVerify = Header(
        alias="auth-token", validation_alias="auth_token", convert_underscores=True
    ),
) -> JSONResponse:
    try:
        payload = AuthUtil.decode_token(auth_token=headers.auth_token)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "id": payload["id"],
                "is_admin": payload["is_admin"],
            },
        )
    except HTTPException as error:
        log.error(f"jwt verify error {error}")

        return JSONResponse(
            status_code=error.status_code, content={"message": "jwt verify error"}
        )
    except Exception as error:
        log.error(f"jwt verify server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt verify server error"},
        )

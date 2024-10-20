from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Header
from starlette.responses import JSONResponse

import schemas
from logger import log
from utils.auth_util import AuthUtil

router = APIRouter()


@router.post("/jwt", status_code=HTTPStatus.CREATED)
async def jwt_create(payload: schemas.JwtCreate) -> JSONResponse:
    token = AuthUtil.encode_token(_id=payload.id, _admin=payload.admin)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=token)


@router.get("/jwt", status_code=HTTPStatus.OK)
async def jwt_verify(
    headers: schemas.JwtVerify = Header(
        alias="auth-token", validation_alias="auth_token", convert_underscores=True
    ),
) -> JSONResponse:
    log.info(f"jwt_verify called...: {headers=}")

    payload = AuthUtil.decode_token(auth_token=headers.auth_token)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "id": payload["id"],
            "admin": payload["is_admin"],
        },
    )

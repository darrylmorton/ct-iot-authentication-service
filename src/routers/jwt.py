from http import HTTPStatus

from fastapi import APIRouter, Header, Body
from starlette.responses import JSONResponse

import schemas
from utils.auth_util import AuthUtil
from utils.observability_util import ObservabilityUtil

router = APIRouter()


@router.post("/jwt", status_code=HTTPStatus.OK)
async def jwt_create(
    payload: schemas.JwtCreate = Body(embed=False),
) -> JSONResponse:
    ObservabilityUtil.request_time("POST", "/jwt", 200)

    token = AuthUtil.encode_token(_id=payload.id, _admin=payload.admin)

    return JSONResponse(status_code=HTTPStatus.OK, content=token)


@router.get("/jwt", status_code=HTTPStatus.OK)
async def jwt_verify(
    headers: schemas.JwtVerify = Header(
        alias="auth-token", validation_alias="auth_token", convert_underscores=True
    ),
) -> JSONResponse:
    ObservabilityUtil.request_time("GET", "/jwt", 200)

    payload = AuthUtil.decode_token(auth_token=headers.auth_token)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "id": payload["id"],
            "admin": payload["is_admin"],
        },
    )

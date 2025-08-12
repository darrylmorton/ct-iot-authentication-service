from http import HTTPStatus

from fastapi import APIRouter, Header, Body, HTTPException
from starlette.responses import JSONResponse

import schemas
from decorators.metrics import observability
from logger import log
from utils.confirm_account_util import ConfirmAccountUtil

router = APIRouter()

ROUTE_PATH = "/jwt/confirm-account"


@router.post(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method="POST")
async def jwt_create_confirm_account(
    payload: schemas.ConfirmAccount = Body(embed=False),
) -> JSONResponse:
    try:
        token = ConfirmAccountUtil.encode_token(
            username=payload.username, email_type=payload.email_type
        )

        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as error:
        log.error(f"jwt_create_confirm_account error {error}")

        return JSONResponse(
            status_code=error.status_code, content={"message": "jwt create error"}
        )
    except Exception as error:
        log.error(f"jwt_create_confirm_account server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt_create_confirm_account server error"},
        )


@router.get(ROUTE_PATH, status_code=HTTPStatus.OK)
@observability(path=ROUTE_PATH, method="GET")
async def jwt_verify_confirm_account(
    headers: schemas.JwtVerify = Header(
        alias="confirm-account-token",
        validation_alias="confirm_account_token",
        convert_underscores=True,
    ),
) -> JSONResponse:
    try:
        payload = ConfirmAccountUtil.decode_token(token=headers.confirm_account_token)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "username": payload["username"],
                "email_type": payload["email_type"],
            },
        )
    except HTTPException as error:
        log.error(f"jwt_verify_confirm_account error {error}")

        return JSONResponse(
            status_code=error.status_code,
            content={"message": "jwt_verify_confirm_account error"},
        )
    except Exception as error:
        log.error(f"jwt_verify_confirm_account server error {error}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "jwt_verify_confirm_account server error"},
        )

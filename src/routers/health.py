from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

import config

router = APIRouter()

ROUTER_PATH = "/healthz"


@router.get(ROUTER_PATH)
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": config.APP_VERSION},
    )

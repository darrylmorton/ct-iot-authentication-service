from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

import config
from decorators.metrics import observability

router = APIRouter()

ROUTER_PATH = "/healthz"


@router.get(ROUTER_PATH)
@observability(path=ROUTER_PATH, method="GET", status_code=HTTPStatus.OK)
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": config.APP_VERSION},
    )

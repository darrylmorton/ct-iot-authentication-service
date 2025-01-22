from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

import config
from utils.observability_util import ObservabilityUtil

router = APIRouter()


@router.get("/healthz")
async def health() -> JSONResponse:
    ObservabilityUtil.request_time("GET", "/healthz", 200)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": config.APP_VERSION},
    )

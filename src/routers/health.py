from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

import config
from decorators.metrics import observability

router = APIRouter()


@router.get("/healthz")
@observability
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": config.APP_VERSION},
    )

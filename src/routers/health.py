from fastapi import APIRouter
from starlette.responses import JSONResponse

import config

router = APIRouter()


@router.get("/healthz")
async def health() -> JSONResponse:
    # division_by_zero = 1 / 0

    return JSONResponse(
        status_code=200, content={"message": "ok", "version": config.APP_VERSION}
    )

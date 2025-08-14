import asyncio
import contextlib
from http import HTTPStatus

import psutil
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from prometheus_client import make_asgi_app
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.responses import JSONResponse

from decorators.metrics import CPU_USAGE, MEMORY_USAGE
from logger import log
import config
from routers import health, jwt_authentication, jwt_confirm_account
from utils.app_util import AppUtil


async def update_process_metrics(interval: float = 5.0):
    process = psutil.Process()

    while True:
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(process.memory_info().rss)

        await asyncio.sleep(interval)


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {config.SERVICE_NAME}...{app.host}")
    log.info(f"Sentry {config.SENTRY_ENVIRONMENT} environment")
    log.info(f"Application {config.ENVIRONMENT} environment")

    if config.SENTRY_ENVIRONMENT != "local":
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=config.SENTRY_TRACES_SAMPLE_RATE,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=config.SENTRY_PROFILES_SAMPLE_RATE,
            sample_rate=config.SENTRY_SAMPLE_RATE,
            environment=config.ENVIRONMENT,
            server_name=config.SERVICE_NAME,
            integrations=[
                StarletteIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
                FastApiIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes=[403, range(500, 599)],
                ),
            ],
        )

    log.info("Starting update_process_metrics() task...")
    asyncio.create_task(update_process_metrics())

    log.info(f"{config.SERVICE_NAME} is ready")

    yield

    log.info(f"{config.SERVICE_NAME} is shutting down...")


app = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics/", metrics_app)

app.include_router(health.router, include_in_schema=False)

app.include_router(jwt_authentication.router, prefix="/api", tags=["authentication"])

app.include_router(jwt_confirm_account.router, prefix="/api", tags=["confirm-account"])
app = AppUtil.set_openapi_info(app=app)

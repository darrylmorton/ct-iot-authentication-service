import contextlib
from http import HTTPStatus

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette import status
from starlette.responses import JSONResponse

from logger import log
import config
from routers import health, jwt
from utils.app_util import AppUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


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

    log.info(f"{config.SERVICE_NAME} is ready")

    yield
    log.info(f"{config.SERVICE_NAME} is shutting down...")


app = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    log.info(f"**** validation_exception_handler called..")

    return JSONResponse(
        # status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.include_router(health.router, include_in_schema=False)
app.include_router(jwt.router, prefix="/api", tags=["jwt"])

app = AppUtil.set_openapi_info(app=app)

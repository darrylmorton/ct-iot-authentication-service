import contextlib

import sentry_sdk
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from logger import log
import config
from routers import health, jwt
from utils.app_util import AppUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {config.SERVICE_NAME}...{app.host}")

    if config.ENVIRONMENT == "production":
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


app.include_router(health.router, include_in_schema=False)
app.include_router(jwt.router, prefix="/api", tags=["jwt"])

app = AppUtil.set_openapi_info(app=app)

import contextlib

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from logger import log
import config
from routers import health, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme.auto_error = False


@contextlib.asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    log.info(f"Starting {config.SERVICE_NAME}...{app.host}")

    log.info(f"{config.SERVICE_NAME} is ready")

    yield
    log.info(f"{config.SERVICE_NAME} is shutting down...")


server = FastAPI(title="FastAPI server", lifespan=lifespan_wrapper)


server.include_router(health.router, include_in_schema=False)

server.include_router(jwt.router, prefix="/api", tags=["jwt"])

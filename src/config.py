import logging
import os

from dotenv import load_dotenv

from utils import app_util

load_dotenv()

APP_VERSION = app_util.get_app_version()
SENTRY_DSN = os.environ.get("SENTRY_DSN")
AWS_REGION = os.environ.get("AWS_REGION")

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("APP_PORT") or 8001
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_TOKEN_EXPIRY_SECONDS = int(os.environ.get("JWT_TOKEN_EXPIRY_SECONDS"))

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/jwt"]


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger

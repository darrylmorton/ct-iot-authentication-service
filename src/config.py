import os

from dotenv import load_dotenv

from utils.app_util import AppUtil

load_dotenv()


APP_VERSION = AppUtil.get_app_version()
HTTP_STATUS_CODE_EXPIRED_TOKEN = 498

AWS_REGION = os.environ.get("AWS_REGION")
SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT") or "local"
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8000
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS"))

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/jwt"]

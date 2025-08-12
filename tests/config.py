import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT") or "local"
ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8001
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS"))
EMAIL_VERIFICATION_TYPES = ["CONFIRM_ACCOUNT_VERIFICATION"]
JWT_SECRET_CONFIRM_ACCOUNT = os.environ.get("JWT_SECRET_CONFIRM_ACCOUNT")
JWT_EXPIRY_SECONDS_CONFIRM_ACCOUNT = int(
    os.environ.get("JWT_EXPIRY_SECONDS_CONFIRM_ACCOUNT")
)

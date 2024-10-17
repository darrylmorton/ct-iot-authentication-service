import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

ENVIRONMENT = os.environ.get("ENVIRONMENT")
SENTRY_ENVIRONMENTS = os.environ.get("SENTRY_ENVIRONMENTS") or ["production"]
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8000
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_TOKEN_EXPIRY_SECONDS = int(os.environ.get("JWT_TOKEN_EXPIRY_SECONDS"))
JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/login"]

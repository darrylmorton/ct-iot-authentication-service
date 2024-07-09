import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

SENTRY_DSN = os.getenv("SENTRY_DSN")
AWS_REGION = os.environ.get("AWS_REGION")

ENVIRONMENT = os.environ.get("ENVIRONMENT") or "TEST"
LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
SERVICE_NAME = os.environ.get("SERVICE_NAME") or "auth-service"
APP_PORT = os.environ.get("APP_PORT") or 8001
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_TOKEN_EXPIRY_SECONDS = int(os.environ.get("JWT_TOKEN_EXPIRY_SECONDS"))

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/login"]

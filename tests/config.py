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

# USER_SERVICE_HOST = os.environ.get("USER_SERVICE_HOST") or "user-service"
# USER_SERVICE_PORT = os.environ.get("USER_SERVICE_PORT")
# USER_SERVICE_URI = os.environ.get("USER_SERVICE_URI")
# USER_SERVICE_URL = f"http://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}/{USER_SERVICE_URI}"

DB_USERNAME = os.environ.get("DB_USERNAME") or "postgres"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or "postgres"
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_PORT = os.environ.get("DB_PORT") or 5432
DB_NAME = os.environ.get("DB_NAME") or "users"

DATABASE_URL_PREFIX = "postgresql+asyncpg"
DATABASE_URL_SUFFIX = (
    "{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USERNAME=DB_USERNAME,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_NAME=DB_NAME,
    )
)
DATABASE_URL = f"{DATABASE_URL_PREFIX}://{DATABASE_URL_SUFFIX}"

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/login"]

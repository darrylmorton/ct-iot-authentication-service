# ct-iot-authentication-service

## Description
The `authentication-service` verifies JWTs, and creates them for login.

[Diagrams](./docs/DIAGRAMS.md)

## Requirements
python v3.11.9+  
poetry v1.7.1

## Install
```
poetry install
```

## Environment Variables
```
AWS_REGION=
SENTRY_ENVIRONMENT=
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=
SENTRY_PROFILES_SAMPLE_RATE=
SENTRY_SAMPLE_RATE=

SERVICE_NAME=
APP_PORT=
LOG_LEVEL=
ENVIRONMENT=

JWT_SECRET=
JWT_TOKEN_EXPIRY_SECONDS=
```

## Build
```
make local-build
```

## Run
Required for running `ct-iot-user-service` locally via [docker-compose-local.yml](https://github.com/darrylmorton/ct-iot-user-service/blob/8e8fe6e0ce43d04b7a4f610e824c748f60e16df2/docker-compose-local.yml)
```
make local-build
```

### Development
```
make dev-server-start
```

### Tests
```
make test
```

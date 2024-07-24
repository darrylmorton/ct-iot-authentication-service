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
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=
SENTRY_PROFILES_SAMPLE_RATE=
SENTRY_SAMPLE_RATE=

SERVICE_NAME=
LOG_LEVEL=
ENVIRONMENT=

JWT_SECRET=
JWT_TOKEN_EXPIRY_SECONDS=
```

## Build
```
make build
```

## Run
### Develoment
```
make dev-server-start
```

### Production
```
make server-start
```

### Test
```
docker-compose up -d
```

### Run Tests
```
make test
```

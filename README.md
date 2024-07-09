# ct-iot-things-report-request-service

## Description

The `authentication-service` verifies JWTs, and creates them for login.

[Diagrams](./docs/DIAGRAMS.md)

## Requirements

python v3.11.9+  
poetry v1.7.1
[user-service](https://github.com/darrylmorton/ct-iot-user-service)

## Run

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

## Deployment

Must be deployed **after** `user-service`.

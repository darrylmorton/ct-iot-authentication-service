# ct-iot-authentication-service

## Description
The `authentication-service` verifies JWTs, and creates them for login.

[Diagrams](./docs/diagrams)

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
JWT_EXPIRY_SECONDS=
```

## Build
```
# for minikube (local development)
eval $(minikube docker-env)

make local-build
```

## Run
Required for running `ct-iot-user-service` locally via [docker-compose-local.yml](https://github.com/darrylmorton/ct-iot-user-service/blob/main/docker-compose-local.yml)
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

### Helm | K8s 
```
helm plugin install https://github.com/jkroepke/helm-secrets --version v4.6.2
helm secrets encrypt helm/authentication-service/secrets-decrypted/credentials.yaml.dec > helm/authentication-service/secrets/credentials.yaml helm/authentication-service -n ct-iot

# development
helm secrets install authentication-service helm/authentication-service -f helm/authentication-service/local-values.yaml -f helm/authentication-service/secrets/credentials.yaml -n ct-iot
helm upgrade authentication-service helm/authentication-service -f helm/authentication-service/local-values.yaml -n ct-iot

k -n ct-iot port-forward svc/authentication-service 8001:9001 &

# production
helm secrets install authentication-service helm/authentication-service -f helm/authentication-service/values.yaml -f helm/authentication-service/secrets/credentials.yaml -n ct-iot
helm upgrade authentication-service helm/authentication-service -f helm/authentication-service/values.yaml -n ct-iot

helm uninstall authentication-service -n ct-iot
```

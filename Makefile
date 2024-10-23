fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

local-build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-authentication-service --target=runtime --progress=plain .
.PHONY: local-build

build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-authentication-service --platform=linux/amd64 --target=runtime --progress=plain .
.PHONY: build

dev-server-start: fmt
	poetry run uvicorn authentication_service.service:app --reload --port 8000
.PHONY: dev-server-start

server-start: fmt
	poetry run uvicorn authentication_service.service:app
.PHONY: server-start

test-unit: fmt
	poetry run pytest tests/unit/
.PHONY: test-unit

test: fmt
	poetry run pytest tests/
.PHONY: test

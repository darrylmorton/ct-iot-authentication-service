fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

check-version: lint
	poetry run python scripts/check_version.py --latest-release-version $(RELEASE_VERSION)
.PHONY: check-version

app-version: lint
	poetry run python scripts/app_version.py
.PHONY: app-version

local-build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-authentication-service:dev --target=runtime --progress=plain .
.PHONY: local-build

build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-authentication-service --platform=linux/amd64 --target=runtime --progress=plain .
.PHONY: build

dev-server-start: fmt
	poetry run uvicorn authentication_service.service:app --reload --port 8001
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

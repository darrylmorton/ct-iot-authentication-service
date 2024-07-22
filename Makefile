fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

build: lint
	DOCKER_BUILDKIT=1 docker build --platform=linux/amd64 --target=runtime --progress=plain .
.PHONY: build

dev-server-start: fmt
	poetry run uvicorn --log-level=debug authentication_service.service:server --reload --port 8001
.PHONY: dev-server-start

server-start: fmt
	poetry run uvicorn authentication_service.service:server
.PHONY: server-start

test-unit: fmt
	poetry run pytest tests/unit/
.PHONY: test-unit

test: fmt
	poetry run pytest tests/
.PHONY: test

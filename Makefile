fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

dev-server-start: fmt
	poetry run uvicorn --log-level=debug authentication_service.service:server --reload
.PHONY: dev-server-start

server-start: fmt
	poetry run uvicorn authentication_service.service:server &
.PHONY: server-start

test-unit: fmt
	poetry run pytest tests/unit/
.PHONY: test-unit

test: fmt
	poetry run pytest tests/
.PHONY: test

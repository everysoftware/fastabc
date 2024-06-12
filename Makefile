APP_NAME=onepattern

.PHONY: format
format:
	ruff format $(APP_NAME) tests

.PHONY: lint
lint:
	ruff check $(APP_NAME) tests --fix
	mypy $(APP_NAME) --install-types

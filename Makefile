APP_NAME=onepattern

.PHONY: format
format:
	ruff format $(APP_NAME) tests docs

.PHONY: lint
lint:
	ruff check $(APP_NAME) tests docs --fix
	mypy $(APP_NAME) tests docs --install-types

.PHONY: test
test:
	pytest tests -s -v

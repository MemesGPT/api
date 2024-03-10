ENVFILE = ../docker/compose/.env.dev
include $(ENVFILE)

PENV = .venv
PYTHON = $(PENV)/bin/python


PROJECT_FOLDERS = bin lib tests

.PHONY: init
init:
	@echo 'Installing python dependencies...'
	@poetry install

.PHONY: lint
lint:
	@echo 'Running ruff checks...'
	@$(PYTHON) -m ruff check

.PHONY: dev-server-start
dev-server-start:
	@echo 'Starting dev server...'
	@SERVER_HOST=$(SERVER_HOST) SERVER_PORT=$(SERVER_PORT) $(PYTHON) -m bin.web

.PHONY: test
test:
	@echo 'Starting dev server...'
	@$(PYTHON) -m pytest tests

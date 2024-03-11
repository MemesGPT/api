ENVFILE = ../docker/compose/.env
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
	@SERVER_HOST=$(SERVER_HOST) \
		SERVER_PORT=$(SERVER_PORT) \
		OPENAI_API_KEY=$(OPENAI_API_KEY) \
		GIGACHAT_API_KEY=$(GIGACHAT_API_KEY) \
		$(PYTHON) -m bin.web

.PHONY: test
test:
	@echo 'Starting dev server...'
	@$(PYTHON) -m pytest tests

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

	@echo 'Running mypy checks...'
	@$(PYTHON) -m mypy .

.PHONY: dev-server-start
dev-server-start:
	@echo 'Starting dev server...'
	@SERVER_HOST=$(SERVER_HOST) \
		SERVER_PORT=$(SERVER_PORT) \
		OPENAI_API_KEY=$(OPENAI_API_KEY) \
		GIGACHAT_API_KEY=$(GIGACHAT_API_KEY) \
		POSTGRES_DB=$(POSTGRES_DB) \
		POSTGRES_TEST_DB=$(POSTGRES_TEST_DB) \
		POSTGRES_USER=$(POSTGRES_USER) \
		POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		$(PYTHON) -m bin.web

.PHONY: test
test:
	@echo 'Starting dev server...'
	@SERVER_HOST=$(SERVER_HOST) \
		SERVER_PORT=$(SERVER_PORT) \
		OPENAI_API_KEY=$(OPENAI_API_KEY) \
		GIGACHAT_API_KEY=$(GIGACHAT_API_KEY) \
		POSTGRES_DB=$(POSTGRES_DB) \
		POSTGRES_TEST_DB=$(POSTGRES_TEST_DB) \
		POSTGRES_USER=$(POSTGRES_USER) \
		POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		$(PYTHON) -m pytest tests -W ignore::DeprecationWarning

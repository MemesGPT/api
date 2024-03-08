COMPOSE_ENV=COMPOSE_PROJECT_NAME=memes_gpt
COMPOSE_BASE_FILE=compose/docker-compose.yml
COMPOSE_DEV_FILE=compose/docker-compose.dev.yml

# Dev mode

.PHONY: dev-build
dev-build:
	$(COMPOSE_ENV) docker compose -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_DEV_FILE) build

.PHONY: dev-start
dev-start:
	$(COMPOSE_ENV) docker compose -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_DEV_FILE) up --detach

.PHONY: dev-stop
dev-stop:
	$(COMPOSE_ENV) docker compose -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_DEV_FILE) down

.PHONY: dev-clean
dev-clean:
	$(COMPOSE_ENV) docker compose -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_DEV_FILE) down --volumes

.PHONY: dev-show-logs
dev-show-logs:
	$(COMPOSE_ENV) docker compose -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_DEV_FILE) logs --follow

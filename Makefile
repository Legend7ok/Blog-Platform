COMPOSE := docker compose -f docker-compose.yaml
COMPOSE_TEST := $(COMPOSE) --profile test

.PHONY: help up up-build build down restart logs ps shell migrate makemigrations test collectstatic superuser

help:
	@echo "Available commands:"
	@echo "  make up-build       Start containers with image build"
	@echo "  make up             Start containers"
	@echo "  make build          Build images"
	@echo "  make down           Stop and remove containers"
	@echo "  make restart        Restart containers"
	@echo "  make logs           Show container logs (follow)"
	@echo "  make ps             Show running services"
	@echo "  make shell          Open shell in web container"
	@echo "  make migrate        Apply Django migrations"
	@echo "  make makemigrations Create Django migrations"
	@echo "  make test           Run tests in test profile"
	@echo "  make collectstatic  Collect static files"
	@echo "  make superuser      Create Django superuser"

up-build:
	$(COMPOSE) up -d --build

up:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

shell:
	$(COMPOSE) exec web sh

migrate:
	$(COMPOSE) run --rm web python app/manage.py migrate

makemigrations:
	$(COMPOSE) run --rm web python app/manage.py makemigrations

test:
	$(COMPOSE_TEST) run --rm test

collectstatic:
	$(COMPOSE) run --rm web python app/manage.py collectstatic --no-input

superuser:
	$(COMPOSE) run --rm web python app/manage.py createsuperuser

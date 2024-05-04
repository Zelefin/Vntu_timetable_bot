.PHONY: deploy
deploy:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: generate
generate:
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	alembic upgrade head
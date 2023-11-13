generate:
	alembic revision --m="$(NAME)" --autogenerate

migrate:
	alembic upgrade head

makedir:
	mkdir "./ScrapItUp/Groups/"
	mkdir "./ScrapItUp/Groups_html/"
	mkdir "./ScrapItUp/Groups_json/"
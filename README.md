# first_fastapi_prjct
Описание: Бэкенд сервиса доставки с переодической задачей
Быстрый старт: docker compose up --build
Переменные окружения: POSTGRES_HOST, REDIS_HOST
Установка: 
1) poetry install
2) docker compose up -d db redis
3) poetry run alembic upgrade head
4) docker compose up --build
Тесты: pytest -v
Стек технологий: FASTAPI 0.136.1, PostgreSQL 17, SQLAlchemyб 
API: /docs
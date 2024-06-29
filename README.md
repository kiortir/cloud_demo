## Применение миграций

### генерация миграций
`docker compose run cloud-migration alembic revision --autogenerate "{Сообщение}"`

### применение миграций
`docker compose run cloud-migration alembic upgrade head`

## Пример .db.env/.db.migration.env
```
db_host=...
db_port=5432
db_username=cloud
db_password=...
db_db=...
```

## Пример .env для  правильной подсветки импротов в vsCode
PYTHONPATH=./cloud

## Запуск сервера
> Обязательно из папки ./cloud или с проставкой PYTHONPATH, иначе импорты умрут
`uvicorn asgi:app --reload`
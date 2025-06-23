# API для заметок с категориями CRUD
Простое REST API для управления заметками и категориями на FastAPI + PostgreSQL.
## Технологии

**Язык** python3.12

**СУБД** postgresql 13

**ORM** SQLAlchemy (+asyncpg для асинохроности)

**Сериализация** Pydantic

**Деплой и контейнеризация** Docker и docker-compose

## Запуск
В проекте есть dockerfile и docker-compose.yml файлы, для того, чтобы запустить приложение достаточно выполнить команду

```bash
docker compose up --build -d
```
Через некоторое время все поднимется и можно будет тестировать.

Зайдя на ```http://localhost:8000/docs``` откроется документация в виде **swagger**, где будут все эндпоинты и схемы. Там же можно и протестировать приложения. Также для удобства тестирование, честно признаю был сгенерирован фронт, просто я не фронтендер - **весь бэкенд мой если что:)**, для этого можно перейти просто на корневую страницу ```http://localhost:8000/```

## Данные

Ниже в простом виде отображены модели данных в упрощенном виде для читаемости, некоторые поля в БД просто на всякий случай, как варианты, что можно использовать. Наример, цвета, архивирование, теги и так далее.
### Notes

```yml
id: UUID  
title: str  
content: str
created_at: datetime  
updated_at: datetime
is_pinned: bool
is_archived: bool
tags: list = []  
category_id: UUID
``` 

### Category
```yml
id: UUID  
name: str  
color: str
```

## Эндпоинты

### Заметки

  **GET /notes/** – список заметок

  **POST /notes/create**– создать

  **GET /notes/{id}**– получить по ID

  **PATCH /notes/{id}/update** – обновить

  **DELETE /notes/{id}/soft_delete** – мягкое удаление(в коде добавляется префикс), может быть полезно для корзины

 **DELETE /notes/{id}/hard_delete** –  жесткое удаление(в коде просто из бд удаляется запись)

### Категории

  **GET /categories/** – список категорий

  **POST /categories/create** – создать

  **GET /categories/{id}** – получить по ID

  **PATCH /categories/{id}/update** – обновить

  **DELETE /categories/{id}/soft_delete** – мягкое удаление(в коде добавляется также префикс)

  **DELETE /categories/{id}/hard_delete** – жесткое удаление(в коде просто из бд удаляется запись)

## Картинки))
### OpenAPI(swagger)
![](/pics/openapi_example.png)

### Пример запроса через CURL
![](/pics/curl_exmaple.png)

### Фронт(сгенеренный)
![](/pics/genereted_front.png)
# FastAPI Microservices: TODO & URL Shortener

В данном репозитории представлены два микросервиса на FastAPI с использованием Docker и SQLite. Данные микросервисы решают следующие проблемы:
1) TODO-сервис: Реализует CRUD-операции для списка задач с
хранением данных в SQLite.
2) Сервис сокращения URL (Short URL): Позволяет создавать короткие
ссылки для длинных URL, перенаправлять по короткому
идентификатору и предоставлять информацию о ссылке. Также
хранение данных в SQLite.

## Структура проекта

```
my-fastapi-project/
├── todo_app/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── sql/
│       ├── init.sql
│       ├── create_item.sql
│       ├── get_all_items.sql
│       ├── get_item_by_id.sql
│       ├── update_item.sql
│       └── delete_item.sql
├── shorturl_app/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── sql/
│       ├── init.sql
│       ├── insert_url.sql
│       ├── get_url_by_id.sql
│       └── check_existing.sql
└── README.md
```

## Сервисы

### 1. TODO Service
Управление списком задач (CRUD операции).

**Порт:** 8000

**Эндпоинты:**
- `POST /items` - создать задачу
- `GET /items` - получить все задачи
- `GET /items/{item_id}` - получить задачу по ID
- `PUT /items/{item_id}` - обновить задачу
- `DELETE /items/{item_id}` - удалить задачу

### 2. URL Shortener Service
Сокращение URL-адресов.

**Порт:** 8001

**Эндпоинты:**
- `POST /shorten` - создать короткую ссылку
- `GET /{short_id}` - перенаправление по короткой ссылке
- `GET /stats/{short_id}` - статистика по ссылке

## Инструкция по локальному запуску

### Требования
- Python 3.8+
- Docker

### Запуск без Docker

#### TODO Service
```bash
cd todo_app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### URL Shortener
```bash
cd shorturl_app
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Запуск с Docker

### Создание томов
```bash
docker volume create todo_data
docker volume create shorturl_data
```

### Сборка образов
```bash
docker build -t <your_username>/todo-service:latest todo_app/
docker build -t <your_username>/shorturl-service:latest shorturl_app/
```

### Запуск контейнеров
```bash
docker run -d -p 8000:80 -v todo_data:/app/data <your_username>/todo-service:latest
docker run -d -p 8001:80 -v shorturl_data:/app/data <your_username>/shorturl-service:latest
```

## Использование образов из Docker Hub

```bash
docker run -d -p 8000:80 -v todo_data:/app/data <your_username>/todo-service:latest
docker run -d -p 8001:80 -v shorturl_data:/app/data <your_username>/shorturl-service:latest
```

## API Документация

- TODO Service: http://localhost:8000/docs
- URL Shortener: http://localhost:8001/docs

## Примеры запросов

### TODO Service

#### Создать задачу
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить продукты", "description": "В магазине"}'
```

#### Получить все задачи
```bash
curl http://localhost:8000/items
```

#### Получить задачу по ID
```bash
curl http://localhost:8000/items/1
```

#### Обновить задачу
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

#### Удалить задачу
```bash
curl -X DELETE http://localhost:8000/items/1
```

### URL Shortener

#### Создать короткую ссылку
```bash
curl -X POST http://localhost:8001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

#### Получить статистику
```bash
curl http://localhost:8001/stats/abc12345
```

## Публикация на Docker Hub

```bash
docker login
docker push <your_username>/todo-service:latest
docker push <your_username>/shorturl-service:latest
```

## Ссылки

- GitHub: [[ссылка](https://github.com/i1uh4/Mentor-s_Seminar.git)]
- Docker Hub TODO сервис: [[ссылка](https://hub.docker.com/repository/docker/i1uh4s/todo-service)]
- Docker Hub Shortener сервис: [[ссылка](https://hub.docker.com/repository/docker/i1uh4s/shorturl-service/general)]
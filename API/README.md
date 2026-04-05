# Habit Tracker API

REST API для трекера привычек на **FastAPI** + **SQLAlchemy** + **SQLite**.

## Стек

| Компонент     | Технология                          |
|---------------|-------------------------------------|
| Framework     | FastAPI 0.111                        |
| ORM           | SQLAlchemy 2.0                       |
| DB (dev)      | SQLite                               |
| DB (prod)     | PostgreSQL (смени DATABASE_URL)      |
| Auth          | JWT (python-jose) + bcrypt (passlib) |
| Валидация     | Pydantic v2                          |
| Тесты         | pytest + httpx                       |

## Быстрый старт

```bash
# 1. Клонировать / распаковать проект
cd habit_tracker

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. (опционально) Создать .env
echo "SECRET_KEY=your-super-secret-key-here" > .env

# 5. Запустить сервер
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) — интерактивная документация Swagger.

## Структура проекта

```
habit_tracker/
├── app/
│   ├── main.py          # точка входа, регистрация роутеров
│   ├── config.py        # настройки через pydantic-settings
│   ├── database.py      # движок SQLAlchemy, get_db dependency
│   ├── models.py        # ORM-модели: User, Habit, HabitLog
│   ├── schemas.py       # Pydantic схемы (request / response)
│   ├── auth.py          # JWT, хэширование, get_current_user
│   └── routers/
│       ├── auth.py      # POST /auth/register, /auth/login, GET /auth/me
│       ├── habits.py    # CRUD /habits/
│       ├── logs.py      # check-in /habits/{id}/logs/
│       └── stats.py     # streak и completion rate /stats/
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```

## Эндпоинты

### Auth
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Логин → JWT token |
| GET  | `/auth/me` | Профиль текущего пользователя |

### Habits
| Метод | URL | Описание |
|-------|-----|----------|
| GET    | `/habits/` | Список привычек |
| POST   | `/habits/` | Создать привычку |
| GET    | `/habits/{id}` | Получить привычку |
| PATCH  | `/habits/{id}` | Обновить привычку |
| DELETE | `/habits/{id}` | Удалить привычку |

### Logs (check-in)
| Метод | URL | Описание |
|-------|-----|----------|
| GET    | `/habits/{id}/logs/` | История выполнения |
| POST   | `/habits/{id}/logs/` | Отметить выполнение |
| DELETE | `/habits/{id}/logs/{log_id}` | Отменить отметку |

### Stats
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/stats/` | Статистика по всем привычкам |
| GET | `/stats/{habit_id}` | Статистика одной привычки |

Возвращает: `current_streak`, `longest_streak`, `total_completions`, `completion_rate_last_30d`.

## Тесты

```bash
pip install pytest httpx
pytest tests/ -v
```

## Переход на PostgreSQL

В `.env`:
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost/habit_db
```

Установить драйвер:
```bash
pip install psycopg2-binary
```

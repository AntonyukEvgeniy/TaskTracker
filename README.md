# TaskTracker

**TaskTracker** — серверное приложение для управления задачами сотрудников, разработанное с использованием **Django REST Framework**.

---

## 📌 Функциональные возможности

### 👤 Управление сотрудниками
- Создание, просмотр, обновление и удаление сотрудников
- Просмотр загруженности сотрудников активными задачами
- Получение детальной информации о задачах сотрудника

### ✅ Управление задачами
- CRUD-операции для задач
- Иерархия задач (родительская / дочерняя)
- Отслеживание статусов: `new`, `in_progress`, `completed`, `cancelled`
- Назначение исполнителей
- Сроки выполнения
- Автоматическое логирование времени создания и обновления

---

## 🛠 Технологии

- Python 3.11+
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL
- Docker & Docker Compose

---

## 📦 Зависимости

### Основные:
- `django>=5.2.2`
- `djangorestframework>=3.16.0`
- `psycopg2-binary>=2.9.9`
- `drf-yasg>=1.21.10` — автодокументация API
- `environs>=14.2.0` — переменные окружения

### Для разработки:
- `black>=25.1.0`
- `flake8>=7.2.0`
- `isort>=6.0.1`
- `pytest>=8.4.1`
- `pytest-cov>=6.2.1`
- `django-debug-toolbar>=5.2.0`

---

## 🚀 Установка и запуск

### 🔧 Локальная разработка

```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd TaskTracker

# 2. Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Установить Poetry и зависимости
pip install poetry
poetry install
```

### 🔐 Создайте `.env` файл в корне:

```
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=tasktracker
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

```bash
# 4. Применить миграции
python manage.py migrate

# 5. Запустить сервер
python manage.py runserver
```

---

### 🐳 Запуск через Docker

```bash
# 1. Убедитесь, что установлен Docker и Docker Compose
# 2. Создайте .env как указано выше

# 3. Запуск
docker-compose up --build
```

---

## 🔌 API Endpoints

### 👥 Сотрудники

| Метод | Endpoint                             | Описание                                  |
|-------|--------------------------------------|-------------------------------------------|
| GET   | `/api/employees/`                    | Список сотрудников                        |
| POST  | `/api/employees/`                    | Создать сотрудника                        |
| GET   | `/api/employees/{id}/`               | Детали сотрудника                         |
| PUT   | `/api/employees/{id}/`               | Обновить сотрудника                       |
| DELETE| `/api/employees/{id}/`               | Удалить сотрудника                        |
| GET   | `/api/employees/busy/`               | Список сотрудников с активными задачами   |

### 🗂 Задачи

| Метод | Endpoint                                                | Описание                                         |
|-------|---------------------------------------------------------|--------------------------------------------------|
| GET   | `/api/tasks/`                                           | Список задач                                     |
| POST  | `/api/tasks/`                                           | Создать задачу                                   |
| GET   | `/api/tasks/{id}/`                                      | Детали задачи                                    |
| PUT   | `/api/tasks/{id}/`                                      | Обновить задачу                                  |
| DELETE| `/api/tasks/{id}/`                                      | Удалить задачу                                   |
| GET   | `/api/tasks/get_important_tasks_and_employees/`         | Важные задачи и рекомендованные исполнители      |

---

## 📚 Документация API

Интерактивная документация доступна по адресу:  
👉 [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# Покрытие кода
pytest --cov
```

---

## 📁 Структура проекта

```
TaskTracker/
├── config/             # Конфигурация Django
├── tasks/              # Приложение задач
├── users/              # Приложение сотрудников
├── tests/              # Автотесты
├── docker-compose.yml  # Docker конфигурация
├── pyproject.toml      # Зависимости Poetry
└── README.md           # Документация проекта
```

---

## ⚖️ Лицензия

Проект распространяется под лицензией **MIT**.

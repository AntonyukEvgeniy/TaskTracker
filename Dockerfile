FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (netcat пригодится для ожидания БД)
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Копируем сначала необходимые для poetry install файлы
COPY README.md .
COPY pyproject.toml .
COPY poetry.lock .

# Установка Poetry и зависимостей
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем остальной код проекта
COPY . .

# Если используется порт
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

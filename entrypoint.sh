#!/bin/bash
# Ожидание доступности PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"
# Применение миграций
python manage.py migrate

# Только при первом запуске контейнера
if [ ! -f ".init_done" ]; then
  echo "Инициализация стартовыми данными..."
  python manage.py populate_db
  touch .init_done
fi
# Запуск команды из docker-compose
exec "$@"
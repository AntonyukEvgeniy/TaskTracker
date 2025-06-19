#!/bin/bash
# Только при первом запуске контейнера
if [ ! -f ".init_done" ]; then
  echo "Инициализация стартовыми данными..."
  python manage.py populate_db
  touch .init_done
fi
# Запуск команды из docker-compose
exec "$@"
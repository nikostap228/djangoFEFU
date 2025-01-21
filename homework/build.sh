#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск сервера
gunicorn homework.wsgi:application --bind 0.0.0.0:$PORT
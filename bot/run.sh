#!/bin/bash

if [ -n "$HOST_URL" ]
then
  exec gunicorn --bind=0.0.0.0:8080 --workers=1 wsgi:app
else
  echo "Бот запущен локально"
  $(python3 bot.py )
fi
# Используем официальный Python образ как базовый
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . /app/

# Устанавливаем Gunicorn
RUN pip install gunicorn

# Открываем порт 8000 для связи с хостом
EXPOSE 8000

# Запускаем Gunicorn для вашего проекта
CMD ["gunicorn", "abu_cheta.wsgi:application", "--bind", "0.0.0.0:8000"]

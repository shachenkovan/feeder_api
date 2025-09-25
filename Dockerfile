FROM python:3.10-slim

WORKDIR /app

# Сначала только зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем uvicorn сразу
CMD ["uvicorn", "api.service:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

# Установим зависимости системы
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 \
    && apt-get clean


# Установим рабочую директорию
WORKDIR /app

# Скопируем зависимости
COPY requirements.txt .

# Установим Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем весь проект
COPY . .

# Запуск скрипта по умолчанию
CMD ["python", "run_detection.py"]

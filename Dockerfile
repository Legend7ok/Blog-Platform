FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Рабочая директория
WORKDIR /app

# Копируем только зависимости (кэширование слоёв)
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск Django
CMD ["uv", "run", "python", "app/manage.py", "runserver", "0.0.0.0:8000"]
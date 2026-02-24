FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy dependency metadata for layer caching
COPY pyproject.toml ./

# Install Python dependencies into system site-packages
RUN pip install --no-cache-dir \
    "django>=6.0.1" \
    "django-storages[s3]>=1.14.6" \
    "django-taggit>=6.1.0" \
    "markdown>=3.10.2" \
    "psycopg[binary]>=3.3.2" \
    "python-decouple>=3.8"

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Start Django
CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]

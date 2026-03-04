FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends make curl gettext \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx

COPY pyproject.toml uv.lock /app/

RUN uv pip install --system --no-cache . \
    && uv pip install --system --no-cache pytest pytest-django

RUN printf '#!/bin/sh\nset -e\npython app/manage.py migrate\npytest app/blog/tests.py -q\n' > /usr/local/bin/test-blog \
    && chmod +x /usr/local/bin/test-blog

COPY /app /app

EXPOSE 8000

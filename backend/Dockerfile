FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.local/bin"

RUN mkdir /app
WORKDIR /app/
RUN apk add --no-cache libpq libffi
RUN apk add --no-cache \
    git `# для установки зависимостей из git` \
    libpq `# для psycopg2` \
    openssl openssl-dev cargo \
    make gcc g++ `# для сборки пакетов` \
    postgresql-dev `# для psycopg2` \
    libffi-dev `# для ffi` \
    && pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml *poetry.lock /app/
RUN poetry install --no-interaction --no-ansi
COPY / /app/

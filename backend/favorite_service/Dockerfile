FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock README.md /app/
COPY . /app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction

EXPOSE 8001
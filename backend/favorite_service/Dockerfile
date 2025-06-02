FROM python:3.12-slim

WORKDIR /app/favorite_service

ENV PYTHONPATH=/app/favorite_service/

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock README.md /app/favorite_service/
COPY . /app/favorite_service/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction

EXPOSE 8001
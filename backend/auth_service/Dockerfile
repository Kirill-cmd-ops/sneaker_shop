FROM python:3.12-slim

WORKDIR /app/auth_service

ENV PYTHONPATH=/app/auth_service/

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock README.md /app/auth_service/
COPY . /app/auth_service/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction

EXPOSE 8000

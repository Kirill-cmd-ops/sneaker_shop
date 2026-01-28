FROM python:3.12-bookworm

WORKDIR /app/backend

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

RUN python -m pip freeze


EXPOSE 8008
FROM python:3.12-slim

WORKDIR /app/stock_notification_service
# ENV PYTHONPATH=/app/stock_notification_service/

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --without dev --no-interaction

RUN python -m pip freeze


EXPOSE 8009
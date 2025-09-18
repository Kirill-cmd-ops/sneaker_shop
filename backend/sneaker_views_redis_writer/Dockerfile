FROM python:3.12-slim

WORKDIR /app/sneaker_views_redis_writer
# ENV PYTHONPATH=/app/sneaker_views_redis_writer/

RUN pip install --upgrade pip

COPY . /app/sneaker_views_redis_writer/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

RUN python -m pip freeze


EXPOSE 8007
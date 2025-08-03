FROM python:3.12-slim

WORKDIR /app/sneaker_details_service
# ENV PYTHONPATH=/app/sneaker_details_service/

RUN pip install --upgrade pip

COPY . /app/sneaker_details_service/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --without dev --no-interaction

RUN python -m pip freeze


EXPOSE 8006
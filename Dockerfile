FROM node:18 AS frontend_builder
WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "dev"]





FROM python:3.12
WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt

COPY .env* ./

COPY backend/ ./backend/

COPY alembic.ini ./
COPY alembic/ ./alembic/

ENV DATABASE_URL="postgresql://postgres:meteor906587@db:5432/sneaker_shop"

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

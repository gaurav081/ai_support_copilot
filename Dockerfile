FROM python:3.13-slim

WORKDIR /app

COPY requirements-render.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY seed_database.py ./
COPY data ./data

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
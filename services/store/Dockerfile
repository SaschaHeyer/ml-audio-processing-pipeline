FROM python:3.7-slim

RUN pip install Flask gunicorn google-cloud-bigquery

WORKDIR /app
COPY . .

CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 app:app
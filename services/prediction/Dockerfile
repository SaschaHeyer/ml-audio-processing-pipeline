FROM python:3.7-slim

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && apt-get upgrade -y && apt-get install -y \
        gcc

RUN pip install Flask gunicorn numpy google-cloud-aiplatform

WORKDIR /app
COPY . .

CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 app:app
# FROM ubuntu:latest
FROM python:alpine3.16 AS builder
WORKDIR /app

COPY . /app
COPY Docker_Requirement/python_requirements.txt /app/requirements.txt
COPY Docker_Requirement/server_env.env /app/.env
COPY Docker_Requirement/server_env.env /app/src/.env
COPY Docker_Requirement/django_settings.py /app/src/settings.py

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
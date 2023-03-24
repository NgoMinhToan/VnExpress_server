# FROM ubuntu:latest
FROM python:alpine3.16 AS builder
WORKDIR /app

COPY . /app
COPY Docker_Requirement/python_requirements.txt /app/requirements.txt
COPY Docker_Requirement/server_env.env /app/.env
COPY Docker_Requirement/server_env.env /app/src/.env
COPY Docker_Requirement/django_settings.py /app/src/settings.py

RUN pip install -r requirements.txt

# RUN apk update && apk upgrade --available && sync
COPY Docker_Requirement/cron_task /etc/cron.d/cron_task
COPY Docker_Requirement/update_news.sh .
RUN chmod 0644 /etc/cron.d/cron_task
RUN chmod +x update_news.sh
RUN crontab /etc/cron.d/cron_task
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT [ "crond", "-f" ]
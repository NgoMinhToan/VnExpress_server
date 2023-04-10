# FROM ubuntu:latest
FROM python:alpine3.16 AS builder
WORKDIR /app

COPY . /app
COPY Docker_Requirement/server_env.env /app/src/.env
# COPY Docker_Requirement/crawl_news.py /app/vnexpressAPI/crawl_data/crawl_news.py

RUN pip install -r requirements.txt

COPY Docker_Requirement/cron_task /etc/cron.d/cron_task
COPY Docker_Requirement/update_news.sh .
RUN chmod 0644 /etc/cron.d/cron_task
RUN chmod +x update_news.sh
RUN crontab /etc/cron.d/cron_task

EXPOSE 8000
# RUN python manage.py migrate
ENTRYPOINT [ "python", "manage.py", "runserver"]

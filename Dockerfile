#Dockerfile for setting up a django instance using postgresql
FROM python:3.9.1-alpine
MAINTAINER Francisco Viveros-Jiménez

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmpBuildDeps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmpBuildDeps
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D pyuser
USER pyuser

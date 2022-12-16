# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV WORKDIR=/banana_api
WORKDIR ${WORKDIR}

ENV FLASK_APP=${WORKDIR}/banana/__init__.py

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
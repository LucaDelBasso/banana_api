# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y iputils-ping

ENV WORKDIR=/banana_api
WORKDIR ${WORKDIR}

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


COPY ./app ${WORKDIR}/app


CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "80", "app.main:app"]

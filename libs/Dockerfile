# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV WORKDIR=/banana_scraper
WORKDIR ${WORKDIR}

COPY requirements_scraper.txt requirements_scraper.txt

RUN pip3 install -r requirements_scraper.txt

COPY . .
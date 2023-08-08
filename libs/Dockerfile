# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y iputils-ping

ENV WORKDIR=/banana_scraper
WORKDIR ${WORKDIR}

COPY requirements_scraper.txt requirements_scraper.txt

RUN pip3 install -r requirements_scraper.txt

COPY . .

# ENTRYPOINT ["tail", "-f", "/dev/null"]

CMD ["python", "banana_scraper.py"]

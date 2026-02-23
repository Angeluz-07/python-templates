FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY . .
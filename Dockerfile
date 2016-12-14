FROM debian:latest

RUN apt-get update; apt-get -y install python-pip

COPY . /app

WORKDIR /app
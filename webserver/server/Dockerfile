# syntax=docker/dockerfile:1.4
FROM ubuntu:22.04

WORKDIR /code
COPY requirements.txt /code

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    iproute2 \
    network-manager \
    dbus \
    net-tools \
    curl \
    iputils-ping \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8000

CMD ["flask", "run"]
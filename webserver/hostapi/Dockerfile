# syntax=docker/dockerfile:1.4
FROM ubuntu:22.04

WORKDIR /code
COPY requirements.txt /code

ARG DEBIAN_FRONTEND=noninteractive

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

ENV FLASK_APP api.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8173
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8173

CMD ["flask", "run"]

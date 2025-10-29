# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

WORKDIR /code
COPY requirements.txt /code

RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/* \
    --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP api.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8001
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8001

CMD ["flask", "run"]
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

COPY ./app /app

RUN apk --update-cache \
    add musl \
    linux-headers \
    gcc \
    g++ \
    make \
    gfortran \
    openblas-dev
RUN apk update \
  && apk --no-cache add openjdk11 \
  && rm -rf /var/cache/apk/*

ENV JAVA_HOME="/usr/lib/jvm/default-jvm/"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

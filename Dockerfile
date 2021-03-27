FROM python:3.9.2-slim-buster

ARG SERVER_HOST=0.0.0.0
ARG SERVER_PORT=8000
ARG DEBUG=True
ARG TZ=Europe/Moscow
ARG DB_NAME=bpn_engine
ARG DB_USER=postgres
ARG DB_PASSWORD=postgres
ARG DB_HOST=localhost
ARG DB_PORT=49154

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Europe/Moscow
ENV SERVER_HOST=${SERVER_HOST}
ENV SERVER_PORT=${SERVER_PORT}
ENV DEBUG=${DEBUG}
ENV TZ=${TZ}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}


WORKDIR app
COPY . /app

RUN apt-get update \
    && apt-get install gcc tini -y \
    && apt-get clean \
    && pip install --upgrade -r /app/requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["sh", "-c", "uvicorn server_configs.asgi:app --host ${SERVER_HOST} --port ${SERVER_PORT} --loop uvloop"]

# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV url="http://localhost"
ENV debug="False"

COPY . .

CMD [ "python3", "-u", "app.py"]
FROM python:3.8.5-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /src

ADD requirements.txt /src/
RUN pip install -r requirements.txt

ADD . /src/

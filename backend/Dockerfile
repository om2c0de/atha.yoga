FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/yoga

COPY ./Pipfile /usr/src/Pipfile
WORKDIR /code/

RUN pip install pipenv
RUN pipenv install




COPY . /usr/src/yoga

EXPOSE 8000
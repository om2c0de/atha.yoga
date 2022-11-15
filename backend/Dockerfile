FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

#COPY ../requirements.txt /code/
#RUN pip install -r requirements.txt


COPY yoga/yoga /code/
WORKDIR /code/

EXPOSE 8000
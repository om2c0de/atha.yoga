FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1


RUN apt update && apt install -y python3-dev

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt


COPY yoga /code/
WORKDIR /code/

EXPOSE 8000
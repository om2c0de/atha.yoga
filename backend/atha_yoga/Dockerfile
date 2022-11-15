FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend/atha_yoga
COPY . /backend/atha_yoga

RUN apt-get update
RUN apt-get install curl -y
RUN pip install poetry
RUN curl -sSL https://install.python-poetry.org | python
RUN poetry install
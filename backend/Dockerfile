FROM python:3.10
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH="/root/.local/bin:$PATH"

COPY ./atha_yoga /backend
WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
FROM python:3.11

RUN pip install pipenv

ENV PROJECT_DIR /opt/services/backend/src
RUN mkdir -p ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy

COPY . ${PROJECT_DIR}

EXPOSE 8000

CMD ["/bin/bash", "entrypoint.sh"]
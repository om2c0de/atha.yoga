FROM python:3.10

RUN pip install pipenv

ENV PROJECT_DIR /opt/services/djangoapp/src
RUN mkdir -p ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy

COPY . ${PROJECT_DIR}

EXPOSE 8080

ENTRYPOINT ["/bin/bash",  "entrypoint.sh"]
FROM python:3.9-slim-buster
EXPOSE ${BACKEND_PORT}

ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

WORKDIR ${APP_HOME}

# Copy all needed files
COPY app app
COPY img img
COPY mock_data mock_data
COPY scripts scripts
COPY tests tests
COPY .env .
COPY Pipfile .
COPY setup.cfg ./
COPY Pipfile.lock ./
COPY run_server.py ./
COPY setup.py ./
COPY pyproject.toml ./

RUN pip install --no-cache-dir -U pip
RUN pip install pipenv
RUN pipenv install --system --dev

ENTRYPOINT ["/bin/bash"]
CMD ["./scripts/docker/docker-entrypoint.sh"]

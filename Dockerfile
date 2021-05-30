FROM python:3.9-slim-buster
EXPOSE ${BACKEND_PORT}

ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

# Copy all needed files
# Needed directories
COPY app app
COPY img img
COPY mock_data mock_data
COPY scripts scripts
COPY tests tests
COPY .env ./
COPY setup.cfg ./
COPY setup.py ./
COPY pyproject.toml ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -U pip
RUN pip install -v --no-cache-dir -U  -r requirements.txt --src /app

# Options for entrypoint:
# --populate-tables (load data from ``mock_data.db_test_data module`` into tables)
# --drop-tables  (drop tables after server is shut down)

# NOTE 1.0: just add-delete the options in ENTYPOINT command as you desire
# NOTE 2.0: if you change the options you first need to prune your containers,
# then rebuild using ``docker system prune -a`` and then ``docker compose up --build``
# or, if you prefer you can run ``sh scripts/docker/prune-build.sh``

ENTRYPOINT ["python", "./scripts/server/run_server.py", "--populate-tables", "--drop-tables"]

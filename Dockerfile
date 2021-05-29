FROM tiangolo/uvicorn-gunicorn:python3.8
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
# COPY Pipfile .
COPY setup.cfg .
COPY Pipfile.lock .
COPY run_server.py .
COPY setup.py .
COPY docker-entrypoint.sh .
COPY pyproject.toml .
COPY requirements.txt .

RUN apt-get update
RUN apt-get -y install sudo
RUN pip install --no-cache-dir -U pip  &&\
    sudo pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash"]
CMD [ "./docker-entrypoint.sh"]

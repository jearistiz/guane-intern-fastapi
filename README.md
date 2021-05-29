# FastAPI - PostgreSQL - Celery - Rabbitmq backend

This source code tries to implementat the following architecture.

At this point the python and database containers are dockerized as well as implemented. The missing parts are the celery-related containers and implementation.

On the other side, all the required endpoints are implemented and tested.

To run the docker images just prepare your environment variables in the ``~/.env`` file and run

```bash
$ docker compose up --build
```

If you want to run the tests, first open another terminal window and get the Container ID of the app/backend container using the command

```bash
$ docker ps
```

Afterwards, run a bash shell using this command

```bash
$ docker exec -it <Container ID> bash
```

When you are already inside the container, move to the ``/app`` directory and run

```bash
$ python -m test pytests
```

![architecture](img/arch.png)

**Note:** this app was developed using as main reference [@tiangolo](https://github.com/tiangolo)'s Full stack, modern web application generator available in [this github repository](https://github.com/tiangolo/full-stack-fastapi-postgresql), which is distributed under an MIT License. Some parts of this source code are literal code blocks from the cited reference.

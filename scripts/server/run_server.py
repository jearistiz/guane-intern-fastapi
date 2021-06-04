"""Uvicorn server initialization script.

Run ``python run_server.py --help`` to see the options.
"""
import os
from typing import Optional

from typer import Typer, Option

from utils._celery import start_celery_worker
from utils._postgres import postgres_server_start, postgres_server_teardown
from utils._redis import (
    redis_local_url, redis_server_start, redis_server_teardown
)
from utils._rabbitmq import (
    local_rabbitmq_uri, init_rabbitmq_app, rabbitmq_server_teardown
)


cli_app = Typer()


port_help = (
    'Set the port of the uvicorn server.'
)
docker_help = (
    'Use this option to run the server in the Docker container. This will '
    'setup the PostgreSQL server using $POSTGRES_URI instead of '
    '$POSTGRES_LOCAL_URI'
)
populate_tables_help = (
    'Fill the <dog> and <user> PostgreSQL tables with mock data stored inside '
    '``mock_data.db_test_data`` module.'
)
drop_tables_help = (
    'After the server is shut down, drop all tables inside PostgreSQL '
    'database.'
)
auto_reload_server_help = (
    'Equivalent to --reload flag in uvicorn server CLI. WARNING: '
    'if you use this option in the docker container this script will not '
    'gracefully stop the Celery worker process behind the application. '
    'If you use it together with --drop-tables tables won\'t be dropped '
    'either.'
)


@cli_app.command()
def run_uvicorn_server(
    docker: bool = Option(True, help=docker_help),
    port: Optional[int] = Option(None, help=port_help),
    populate_tables: bool = Option(True, help=populate_tables_help),
    drop_tables: bool = Option(True, help=drop_tables_help),
    auto_reload_server: bool = Option(False, help=drop_tables_help),
) -> None:
    """Run the FastAPI app using an uvicorn server, optionally setting up and
    tearing down some other overheads such as PostgreSQL db, Celery worker,
    RabbitMQ server, Redis server, etc.
    """
    from app.config import sttgs

    # Setup local environment (as opposed to docker). Tested on MacOS v11.2.3
    if not docker:
        # Set env postgres URI
        os.environ['POSTGRES_URI'] = sttgs.get('POSTGRES_LOCAL_URI')
        # Start postgres server
        postgres_datadir = '/usr/local/var/postgres'
        postgres_server_start(postgres_datadir)

        # Set env local RabbitMQ URI
        os.environ['RABBITMQ_URI'] = local_rabbitmq_uri(
            user=sttgs["RABBITMQ_DEFAULT_USER"],
            pwd=sttgs["RABBITMQ_DEFAULT_PASS"],
            port=sttgs["RABBITMQ_PORT"],
            vhost=sttgs["RABBITMQ_DEFAULT_VHOST"]
        )
        # Start RabbitMQ
        rabbitmq_user = sttgs.get('RABBITMQ_DEFAULT_USER', 'guane')
        rabbitmq_pass = sttgs.get('RABBITMQ_DEFAULT_PASS', 'ilovefuelai')
        rabbtmq_vhost = sttgs.get('RABBITMQ_DEFAULT_VHOST', 'fuelai')
        rabbitmq_server_process, _ = init_rabbitmq_app(  # noqa
            rabbitmq_user, rabbitmq_pass, rabbtmq_vhost
        )

        # Set env local Redis URI
        redis_host = sttgs["REDIS_HOST"]
        redis_port = sttgs["REDIS_PORT"]
        os.environ['CELERY_BAKCEND_URI'] = redis_local_url(
            redis_host, redis_port
        )
        # Start Redis server
        redis_server_process = redis_server_start(redis_port)

    # This dependencies need to be imported here so that the sqlAlchemy engine
    # is created with the correct uri (previously modified by local_db
    # oprtion). If they are imported at the beggining of the script, the
    # dependencies inside the import statements will make the server to be run
    # using the wrong URI
    import uvicorn

    from app.db.db_manager import create_all_tables, drop_all_tables
    from app.db.utils import populate_tables_mock_data

    # Tables need to be created, always
    create_all_tables()

    # Optionally populate tables
    populate_tables_mock_data(populate=populate_tables)

    backend_port = port if port else sttgs.get('BACKEND_PORT', 8080)

    # Start celery worker
    celery_worker_process = start_celery_worker(
        module='app.worker.celery_tasks'
    )

    # Run server
    uvicorn.run(
        "app.main:app",
        host=sttgs.get('BACKEND_HOST', '0.0.0.0'),
        port=int(backend_port),
        reload=auto_reload_server,
        debug=auto_reload_server,
        workers=int(sttgs.get('SERVER_WORKERS', 1)),
    )

    # Optionally drop all postgres tables
    drop_all_tables(drop=drop_tables)

    # Terminate local (as opposed to docker) processes
    if not docker:
        rabbitmq_server_teardown(rabbitmq_server_process)
        redis_server_teardown(redis_server_process)
        postgres_server_teardown(postgres_datadir)

    # Always terminate celery worker instance
    celery_worker_process.terminate()


if __name__ == '__main__':
    cli_app()

"""Uvicorn server initialization script.

Run ``python run_server.py --help`` to see the options.
"""
import os
from typing import Optional

import uvicorn
from typer import Typer, Option

from scripts.utils._manage_services import setup_services, teardown_services
from scripts.utils._celery import start_celery_worker


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
debug_celery_help = (
    'Set to True if you want to see calery debug messages in your terminal '
    'session.'
)


@cli_app.command()
def run_uvicorn_server(
    docker: bool = Option(True, help=docker_help),
    port: Optional[int] = Option(None, help=port_help),
    populate_tables: bool = Option(True, help=populate_tables_help),
    drop_tables: bool = Option(True, help=drop_tables_help),
    auto_reload_server: bool = Option(False, help=drop_tables_help),
    debug_celery: bool = Option(False, help=debug_celery_help)
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

        postgres_datadir = '/usr/local/var/postgres'

        # The celery worker must be initialized every single time, not just if
        # it is a 'local' deploy, we initialize it outside this if statement
        rabbitmq_server_process, redis_server_process, _ = setup_services(
            postgres_datadir=postgres_datadir,
            celery_worker=False
        )

    # Start celery worker
    celery_worker_process = start_celery_worker(debug=debug_celery)

    # This dependencies need to be imported here so that the sqlAlchemy engine
    # is created with the correct uri (previously modified by local_db
    # oprtion). If they are imported at the beggining of the script, the
    # dependencies inside the import statements will make the server to be run
    # using the wrong URI
    from app.db.db_manager import create_all_tables, drop_all_tables
    from app.db.utils import populate_tables_mock_data

    # Tables need to be created, always
    create_all_tables()

    # Optionally populate tables
    populate_tables_mock_data(populate=populate_tables)

    backend_port = port if port else sttgs.get('BACKEND_PORT', 8080)

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

    # Always terminate celery worker instance
    celery_worker_process.terminate()

    # Terminate local (as opposed to docker) processes
    if not docker:
        teardown_services(
            rabbitmq_server_process,
            redis_server_process,
            celery_worker_process=None,
            postgres_datadir=postgres_datadir,
        )


if __name__ == '__main__':
    cli_app()

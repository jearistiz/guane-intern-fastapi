"""Uvicorn server initialization script.

Run ``python run_server.py --help`` to see the options.
"""
import os
import subprocess
import time
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

from typer import Typer, Option


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
        redis_server_process = redis_server_start(redis_host, redis_port)

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
        postgres_server_stop(postgres_datadir)

    # Always terminate celery worker instance
    celery_worker_process.terminate()


# Celery
###############################################################################
def start_celery_worker(module: str):
    return subprocess.Popen(['celery', '-A', module, 'worker'])


# PostgreSQL
###############################################################################
def postgres_server_start(datadir: str) -> subprocess.CompletedProcess:
    return subprocess.run(['pg_ctl', '-D', datadir, 'start'])


def postgres_server_stop(datadir: str) -> subprocess.CompletedProcess:
    return subprocess.run(['pg_ctl', '-D', datadir, 'stop'])


# Redis
###############################################################################
def redis_local_url(host: str, port: str) -> str:
    return f'redis://{host}:{port}'


def redis_server_start(
    host: str, port: str, background: bool = True
) -> subprocess.Popen:
    daemonize = 'yes' if background else 'no'
    return subprocess.Popen(
        ['redis-server', '-h', host, '-p', port, '--daemonize', daemonize]
    )


def redis_server_shut_down():
    return subprocess.run(['redis-cli', 'shutdown'])


def redis_server_teardown(
    redis_server_process: subprocess.Popen,
    delete_file_names: List[str] = ['erl_crash.dump', 'dump.rdb']
) -> subprocess.CompletedProcess:
    redis_shut_down_completed_process = redis_server_shut_down()
    subprocess.run(['rm'] + delete_file_names)
    redis_server_process.terminate()
    return redis_shut_down_completed_process


# RabbitMQ
###############################################################################
def local_rabbitmq_uri(
    user: str, pwd: str, port: str, vhost: str
) -> str:
    return f'amqp://{user}:{pwd}@0.0.0.0:{port}/{vhost}'


def init_rabbitmq_app(
    rabbitmq_user: str,
    rabbitmq_pass: str,
    rabbitmq_vhost: str,
    max_retries: int = 10,
    sleep_time: int = 1  # In seconds
) -> Tuple[subprocess.Popen, int]:
    """Starts the RabbitMQ server, creates a new user with its credentials,
    creates a new virtual host and adds administration priviledges to the
    user in the virtual host.
    """

    module_name_tag = f'[{Path(__file__).stem}]'
    hidden_pass = "x" * (len(rabbitmq_pass) - 2) + rabbitmq_pass[-2:]
    user_with_pass = f'user {rabbitmq_user} with password {hidden_pass}'

    _, _ = rabbitmq_full_start_app()

    # Create user
    rabbitmq_user_process = rabbitmq_create_user(rabbitmq_user, rabbitmq_pass)

    if rabbitmq_user_process.returncode == 0:
        print(f'{module_name_tag} rabbitmqctl created {user_with_pass} ')
    else:
        warnings.warn(
            f'{module_name_tag} rabbitmqctl couldn\'t create '
            f'{user_with_pass}, probably because the server couldn\'t be '
            'started appropriately or the user already existed.'
        )

    # Add virtual host
    rabbitmq_add_vhost(rabbitmq_vhost)

    # Set user as administrator
    rabbitmq_set_user_admin(rabbitmq_user)

    # Set read, write and execute permissions on user
    rabbitmq_user_permissions(rabbitmq_vhost, rabbitmq_user)

    # We need to restart the server, this way the newly created user and
    # permissions take effect
    rabbitmq_server_process, server_ping_statuscode = rabbitmq_restart_server(
        max_retries, sleep_time
    )

    return rabbitmq_server_process, server_ping_statuscode


def rabbitmq_start_wait_server(
    retries: int = 15, sleep_time: int = 1
) -> Tuple[subprocess.Popen, int]:
    rabbitmq_server_process = subprocess.Popen(['rabbitmq-server'])

    ping_returncode = 1

    i = 0
    while ping_returncode != 0 and i < retries:
        time.sleep(sleep_time)
        ping_process = subprocess.run(['rabbitmqctl', 'ping'])
        ping_returncode = ping_process.returncode
        del ping_process
        i += 1

    return rabbitmq_server_process, ping_returncode


def rabbitmq_full_start_app(
    retries: int = 15, sleep_time: int = 1
) -> Tuple[subprocess.Popen, int]:
    """Starts both rabbitmq server and application"""
    # Start rabbitmq server
    rabbitmq_server_process, server_ping_code = rabbitmq_start_wait_server(
        retries, sleep_time
    )
    # Start rabbitmq application
    subprocess.run(['rabbitmqctl', 'start_app'])
    subprocess.run(['rabbitmqctl', 'await_startup'])
    return rabbitmq_server_process, server_ping_code


def rabbitmq_create_user(
    rabbitmq_user: str, rabbitmq_pass: str
) -> subprocess.CompletedProcess:
    return subprocess.run(
        ['rabbitmqctl', 'add_user', rabbitmq_user, rabbitmq_pass]
    )


def rabbitmq_add_vhost(rabbitmq_vhost: str) -> subprocess.CompletedProcess:
    return subprocess.run(['rabbitmqctl', 'add_vhost', rabbitmq_vhost])


def rabbitmq_set_user_admin(
    rabbitmq_user: str
) -> subprocess.CompletedProcess:
    # Set user as administrator
    subprocess.run(
        ['rabbitmqctl', 'set_user_tags', rabbitmq_user, 'administrator']
    )


def rabbitmq_user_permissions(
    rabbitmq_vhost: str,
    rabbitmq_user: str,
    permissions: Tuple[str, str, str] = ('.*', '.*', '.*')
):
    """Set read, write and execute permissions on user"""
    cmd_base = [
        'rabbitmqctl', 'set_permissions', '-p', rabbitmq_vhost, rabbitmq_user
    ]
    subprocess.run(cmd_base + list(permissions))


def rabbitmq_restart_server(
    retries: int = 15, sleep_time: int = 1
) -> Tuple[subprocess.Popen, int]:
    subprocess.run(['rabbitmqctl', 'shutdown'])
    return rabbitmq_start_wait_server(retries, sleep_time)


def rabbitmq_reset_and_shut_down_server():
    rabbitmq_start_wait_server()
    subprocess.run(['rabbitmqctl', 'stop_app'])
    subprocess.run(['rabbitmqctl', 'reset'])
    subprocess.run(['rabbitmqctl', 'shutdown'])


def rabbitmq_server_teardown(rabbitmq_server_process: subprocess.Popen):
    rabbitmq_server_process.terminate()
    rabbitmq_reset_and_shut_down_server()


if __name__ == '__main__':
    cli_app()

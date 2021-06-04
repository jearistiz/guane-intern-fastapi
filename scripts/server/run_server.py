"""Uvicorn server initialization script.

Run ``python run_server.py --help`` to see the options.
"""
import os
import subprocess
import time
import warnings
from pathlib import Path
from typing import Optional, Tuple

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
        # Set local database URI
        os.environ['POSTGRES_URI'] = sttgs.get('POSTGRES_LOCAL_URI')

        # Ser local RabbitMQ URI
        os.environ['RABBITMQ_URI'] = (
            'amqp://'
            f'{sttgs["RABBITMQ_DEFAULT_USER"]}:'
            f'{sttgs["RABBITMQ_DEFAULT_PASS"]}@'
            f'0.0.0.0:{sttgs["RABBITMQ_PORT"]}/'
            f'{sttgs["RABBITMQ_DEFAULT_VHOST"]}'
        )

        # Set local Redis URI
        redis_host = sttgs["REDIS_HOST"]
        redis_port = sttgs["REDIS_PORT"]
        os.environ['CELERY_BAKCEND_URI'] = (
            f'redis://{redis_host}:{redis_port}'
        )

        # Start postgres server
        postgres_command = [
            'pg_ctl', '-D', '/usr/local/var/postgres'
        ]
        subprocess.run(postgres_command + ['start'])

        # Start RabbitMQ
        rabbitmq_user = sttgs.get('RABBITMQ_DEFAULT_USER', 'guane')
        rabbitmq_pass = sttgs.get('RABBITMQ_DEFAULT_PASS', 'ilovefuelai')
        rabbtmq_vhost = sttgs.get('RABBITMQ_DEFAULT_VHOST', 'fuelai')
        rabbitmq_server = init_rabbitmq_app(  # noqa
            rabbitmq_user, rabbitmq_pass, rabbtmq_vhost
        )

        # Start Redis server
        redis_server = subprocess.Popen(
            ['redis-server', '-h', redis_host, '-p', redis_port]
        )

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
    celery_worker = subprocess.Popen(
        ['celery', '-A', 'app.worker.celery_tasks', 'worker']
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

    # Optionally drop tables
    drop_all_tables(drop=drop_tables)

    # Terminate local (as opposed to docker) processes
    if not docker:
        rabbitmq_server.terminate()
        rabbitmq_start_wait_server()
        subprocess.run(['rabbitmqctl', 'stop_app'])
        subprocess.run(['rabbitmqctl', 'reset'])
        subprocess.run(['rabbitmqctl', 'shutdown'])
        redis_server.terminate()
        # Stop postgres server
        subprocess.run(postgres_command + ['stop'])

    # Terminate celery worker instance
    celery_worker.terminate()


def init_rabbitmq_app(
    rabbitmq_user: str,
    rabbitmq_pass: str,
    rabbitmq_vhost: str,
    max_retries: int = 10,
    sleep_time: int = 1  # In seconds
) -> subprocess.Popen:
    module_name_tag = f'[{Path(__file__).stem}]'
    hidden_pass = "x" * (len(rabbitmq_pass) - 2) + rabbitmq_pass[-2:]
    user_with_pass = f'user {rabbitmq_user} with password {hidden_pass}'

    # Start rabbitmq server
    rabbitmq_server = subprocess.Popen(['rabbitmq-server'])
    rabbitmq_server_started = False

    # Create user and password, add permissions
    i = 0
    while not rabbitmq_server_started and i < max_retries:
        rabbitmq_ping_return_code = subprocess.run(
            ['rabbitmqctl', 'ping']
        ).returncode

        # If server is active, create user
        if rabbitmq_ping_return_code == 0:
            # Start rabbitmq application
            subprocess.run(['rabbitmqctl', 'start_app'])
            subprocess.run(['rabbitmqctl', 'await_startup'])
            # Create user
            rabbitmq_user_process = subprocess.run(
                ['rabbitmqctl', 'add_user', rabbitmq_user, rabbitmq_pass]
            )
            rabbitmq_server_started = True
            break

        print(
            f'{module_name_tag} rabbitmqctl trying to create '
            f'{user_with_pass}, but rabbitmq-server seems not to be active.'
        )

        time.sleep(sleep_time)

        i += 1

    if rabbitmq_user_process.returncode == 0:
        print(f'{module_name_tag} rabbitmqctl created {user_with_pass} ')
    else:
        warnings.warn(
            f'{module_name_tag} rabbitmqctl couldn\'t create '
            f'{user_with_pass}, probably because the server couldn\'t be '
            'started appropriately or the user already existed.'
        )

    # Add virtual host
    subprocess.run(['rabbitmqctl', 'add_vhost', rabbitmq_vhost])

    # Set user as administrator
    subprocess.run(
        ['rabbitmqctl', 'set_user_tags', rabbitmq_user, 'administrator']
    )

    # Set read, write and execute permissions on user
    all_permissions = '.*'  # f"{rabbitmq_user}-client-queues|amq\.default"
    subprocess.run(
        [
            'rabbitmqctl', 'set_permissions', '-p',
            rabbitmq_vhost, rabbitmq_user,
            all_permissions, all_permissions, all_permissions
        ]
    )

    # Restart server
    subprocess.run(['rabbitmqctl', 'shutdown'])
    rabbitmq_server = subprocess.Popen(['rabbitmq-server'])

    # Restart server
    subprocess.run(['rabbitmqctl', 'shutdown'])
    rabbitmq_server = subprocess.Popen(['rabbitmq-server'])

    return rabbitmq_server


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


if __name__ == '__main__':
    cli_app()

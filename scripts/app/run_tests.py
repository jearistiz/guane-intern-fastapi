"""Testing script for FastAPI app.

From the root of the project run
``$ pipenv run python scripts/app/run_tests.py --help``
to see the options.
"""
import os
import py

import pytest
from typer import Typer, Option

from scripts.utils._celery import start_celery_worker
from scripts.utils._postgres import (
    postgres_server_start,
    postgres_server_teardown
)
from scripts.utils._redis import (
    redis_local_url, redis_server_start, redis_server_teardown
)
from scripts.utils._rabbitmq import (
    local_rabbitmq_uri, init_rabbitmq_app, rabbitmq_server_teardown
)

tests_cli = Typer()


docker_help = (
    'Use this flag when running inside the docker container.'
    'This ensures that a valid $POSGRES_URI is parsed from the ``~/.env`` '
    'file.'
)
server_running_help = (
    'Use this option when you are locally running the server (as opposed to '
    'running it using docker) and it is active. This is because if the '
    'server is running so are Celery, RabbitMQ, and Redis and we can just '
    'use those in our testing environment. Note that if you do not want this '
    'behaviour, you will need to modify this script and fit it to your needs.'
)
cov_help = 'Show coverage of tests with target directory app/'
cov_html_help = (
    'Print coverage and generate html files to see detail of coverage.'
)
print_all_help = 'Print all stdout from the source code that is being tested.'
collect_only_help = 'Only collect tests, don\'t execute them.'
override_options_help = (
    '(TEXT should be quoted). Use this argument to override all other pytest '
    'options in this CLI, except the --docker one. Usage examples: \n'
    '``$ python run_tests.py --docker --override-options "--fixtures"``\n'
    '``$ python run_tests.py --no-docker --override-options "--ff"``.\n'
    'Run ``$ pytest --help`` to see more pytest options. Note that some '
    'options are not compatible withthis CLI.'
)


@tests_cli.command()
def run_tests(
    docker: bool = Option(True, help=docker_help),
    server_running: bool = Option(True, help=server_running_help),
    cov: bool = Option(True, help=cov_help),
    cov_html: bool = Option(False, help=cov_html_help),
    print_all: bool = Option(False, help=print_all_help),
    collect_only: bool = Option(False, help=collect_only_help),
    override_options: str = Option('', help=override_options_help)
) -> None:
    from app.config import sttgs

    if not docker:
        # Set env postgres URI
        os.environ['POSTGRES_TESTS_URI'] = sttgs.get(
            'POSTGRES_LOCAL_TESTS_URI'
        )
        if not server_running:
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
            redis_port = sttgs["REDIS_PORT"]
            os.environ['CELERY_BAKCEND_URI'] = redis_local_url(redis_port)
            # Start Redis server
            redis_server_process = redis_server_start(redis_port)

            # Start celery worker
            celery_worker_process = start_celery_worker(
                module='app.worker.celery_tasks'
            )

    # First pytest_args element: tests directory
    pytest_args = ["tests"]

    if override_options:
        pytest_args += override_options.split(' ')

    else:
        if print_all:
            pytest_args.append("--capture=tee-sys")

        if (cov and cov_html) or cov_html:
            pytest_args += ["--cov-report", "html", "--cov", "app"]

        elif cov and not cov_html:
            pytest_args += ["--cov", "app"]

        if collect_only:
            pytest_args.append('--collect-only')

    # Helps to capture the text "internally printed" by pytest when called
    # via pytest.main()
    capture = py.io.StdCapture()

    # Run tests
    pytest.main(pytest_args)

    # Print all pytest output
    std, _ = capture.reset()
    print(std)

    # Terminate local (as opposed to docker) processes
    if not docker and not server_running:
        # Always terminate celery worker instance
        celery_worker_process.terminate()
        rabbitmq_server_teardown(rabbitmq_server_process)
        redis_server_teardown(redis_server_process)
        postgres_server_teardown(postgres_datadir)


if __name__ == '__main__':
    tests_cli()

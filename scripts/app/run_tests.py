"""Testing script for FastAPI app.

From the root of the project run
``$ pipenv run python scripts/app/run_tests.py --help``
to see the options.
"""
import os
import py

import pytest
from typer import Typer, Option

from scripts.utils._manage_services import setup_services, teardown_services


tests_cli = Typer()


docker_help = (
    'Use this flag when running inside the docker container.'
    'This ensures that a valid $POSGRES_URI is parsed from the ``~/.env`` '
    'file.'
)
repopulate_tables_help = (
    'When the --docker option is set to true, the tables will be empty after '
    'the tests. If you want to repopulate the tables with mock data, use this '
    'option. This option only works together with --docker option.'
)
debug_celery_help = (
    'Set to True if you want to see calery debug messages in your terminal '
    'session.'
)
cov_help = 'Show coverage of tests with target directory app/'
cov_html_help = (
    'Print coverage and generate html files to see detail of coverage.'
)
print_all_help = 'Print all stdout from the source code that is being tested.'
collect_only_help = 'Only collect tests, don\'t execute them.'
override_options_help = (
    '(TEXT should be quoted). Use this argument to override all other pytest '
    'options in this CLI, except --docker --server_running and '
    '--repopulate_tables. Usage examples: \n'
    '``$ python run_tests.py --docker --override-options "--fixtures"``\n'
    '``$ python run_tests.py --no-docker --override-options "--ff"``.\n'
    'Run ``$ pytest --help`` to see more pytest options. Note that some pytest'
    'options are not compatible withthis CLI.'
)


@tests_cli.command()
def run_tests(
    docker: bool = Option(True, help=docker_help),
    repopulate_tables: bool = Option(True, help=repopulate_tables_help),
    debug_celery: bool = Option(False, help=debug_celery_help),
    cov: bool = Option(True, help=cov_help),
    cov_html: bool = Option(False, help=cov_html_help),
    print_all: bool = Option(False, help=print_all_help),
    collect_only: bool = Option(False, help=collect_only_help),
    override_options: str = Option('', help=override_options_help)
) -> None:

    if not docker:
        from app.config import sttgs
        # Set env postgres URI
        os.environ['POSTGRES_TESTS_URI'] = sttgs.get(
            'POSTGRES_LOCAL_TESTS_URI'
        )

        postgres_datadir = '/usr/local/var/postgres'

        services_processes = setup_services(
            postgres_datadir=postgres_datadir,
            celery_worker=True,
            debug_celery_worker=debug_celery
        )

        rabbitmq_server_process = services_processes[0]
        redis_server_process = services_processes[1]
        celery_worker_process = services_processes[2]

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

    # Docker uses the same database for testing and for server deployment
    # we need to recreate the tables and repopulate them
    if docker:
        from app.db.db_manager import create_all_tables
        from app.db.utils.populate_tables import populate_tables_mock_data
        create_all_tables()
        populate_tables_mock_data(populate=repopulate_tables)

    # Print all pytest output
    std, _ = capture.reset()
    print(std)

    # Terminate local (as opposed to docker) processes
    if not docker:
        teardown_services(
            rabbitmq_server_process,
            redis_server_process,
            celery_worker_process=celery_worker_process,
            postgres_datadir=postgres_datadir,
        )


if __name__ == '__main__':
    tests_cli()

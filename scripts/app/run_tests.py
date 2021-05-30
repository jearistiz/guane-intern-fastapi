"""Testing script for FastAPI app.

From the root of the project run
``$ pipenv run python scripts/app/run_tests.py --help``
to see the options.
"""
import os
import py

import pytest
from typer import Typer, Option


tests_cli = Typer()


docker_help = 'Use this flag when running inside the docker container.'
cov_help = 'Print coverage'
cov_html_help = (
    'Print coverage and generate html files to see detail of coverage.'
)
print_all_help = 'Print all stdout from the source code that is being tested.'


@tests_cli.command()
def run_tests(
    docker: bool = Option(False, help=docker_help),
    cov: bool = Option(True, help=cov_help),
    cov_html: bool = Option(False, help=cov_html_help),
    print_all: bool = Option(False, help=print_all_help)
) -> None:

    if not docker:
        from app.config import sttgs
        os.environ['POSTGRES_TESTS_URI'] = sttgs.get(
            'POSTGRES_LOCAL_TESTS_URI'
        )

    # First pytest_args element: tests directory
    pytest_args = ["tests"]

    if print_all:
        pytest_args.append("--capture=tee-sys")

    if (cov and cov_html) or cov_html:
        pytest_args += ["--cov-report", "html", "--cov", "app"]

    elif cov and not cov_html:
        pytest_args += ["--cov", "app"]

    # Helps to capture the text "internally printed" by pytest when called
    # via pytest.main()
    capture = py.io.StdCapture()

    # Run tests
    pytest.main(pytest_args)

    # Print all pytest output
    std, _ = capture.reset()
    print(std)


if __name__ == '__main__':
    tests_cli()

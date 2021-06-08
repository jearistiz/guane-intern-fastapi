import time
import warnings
from pathlib import Path
from typing import Tuple
from subprocess import Popen, run, CompletedProcess


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
) -> Tuple[Popen, int]:
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
) -> Tuple[Popen, int]:
    rabbitmq_server_process = Popen(['rabbitmq-server'])

    ping_returncode = 1

    i = 0
    while ping_returncode != 0 and i < retries:
        time.sleep(sleep_time)
        ping_process = run(['rabbitmqctl', 'ping'])
        ping_returncode = ping_process.returncode
        del ping_process
        i += 1

    return rabbitmq_server_process, ping_returncode


def rabbitmq_full_start_app(
    retries: int = 15, sleep_time: int = 1
) -> Tuple[Popen, int]:
    """Starts both rabbitmq server and application"""
    # Start rabbitmq server
    rabbitmq_server_process, server_ping_code = rabbitmq_start_wait_server(
        retries, sleep_time
    )
    # Start rabbitmq application
    run(['rabbitmqctl', 'start_app'])
    run(['rabbitmqctl', 'await_startup'])
    return rabbitmq_server_process, server_ping_code


def rabbitmq_create_user(
    rabbitmq_user: str, rabbitmq_pass: str
) -> CompletedProcess:
    return run(
        ['rabbitmqctl', 'add_user', rabbitmq_user, rabbitmq_pass]
    )


def rabbitmq_add_vhost(rabbitmq_vhost: str) -> CompletedProcess:
    return run(['rabbitmqctl', 'add_vhost', rabbitmq_vhost])


def rabbitmq_set_user_admin(
    rabbitmq_user: str
) -> CompletedProcess:
    # Set user as administrator
    run(
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
    run(cmd_base + list(permissions))


def rabbitmq_restart_server(
    retries: int = 15, sleep_time: int = 1
) -> Tuple[Popen, int]:
    run(['rabbitmqctl', 'shutdown'])
    return rabbitmq_start_wait_server(retries, sleep_time)


def rabbitmq_reset_and_shut_down_server():
    rabbitmq_start_wait_server()
    run(['rabbitmqctl', 'stop_app'])
    run(['rabbitmqctl', 'reset'])
    run(['rabbitmqctl', 'shutdown'])


def rabbitmq_server_teardown(rabbitmq_server_process: Popen):
    rabbitmq_server_process.terminate()
    rabbitmq_reset_and_shut_down_server()

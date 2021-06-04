from typing import List
from subprocess import Popen, run, CompletedProcess


def redis_local_url(port: str) -> str:
    return f'redis://0.0.0.0:{port}'


def redis_server_start(port: str) -> Popen:
    return Popen(['redis-server', '--port', port])


def redis_server_shut_down():
    return run(['redis-cli', 'shutdown'])


def redis_server_teardown(
    redis_server_process: Popen,
    delete_file_names: List[str] = ['erl_crash.dump', 'dump.rdb']
) -> CompletedProcess:
    redis_shut_down_completed_process = redis_server_shut_down()
    redis_server_process.terminate()
    run(['rm'] + delete_file_names)
    return redis_shut_down_completed_process

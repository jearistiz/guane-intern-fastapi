from subprocess import run, CompletedProcess


def postgres_server_start(datadir: str) -> CompletedProcess:
    return run(['pg_ctl', '-D', datadir, 'start'])


def postgres_server_stop(datadir: str) -> CompletedProcess:
    return run(['pg_ctl', '-D', datadir, 'stop'])


def postgres_server_teardown(datadir: str) -> CompletedProcess:
    return postgres_server_stop(datadir)

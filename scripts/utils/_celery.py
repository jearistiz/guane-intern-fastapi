from subprocess import Popen


def start_celery_worker(
    module: str = 'app.worker.celery_app:celery_app',
    debug: bool = False
) -> Popen:
    celery_command = ['celery', '-A', module, 'worker']
    celery_command += ['--loglevel=DEBUG'] if debug else []
    return Popen(celery_command)

import os
from subprocess import Popen
from typing import Optional, Tuple

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


def setup_services(
    postgres_datadir: str = '/usr/local/var/postgres',
    celery_worker: bool = False,
    debug_celery_worker: bool = False,
) -> Tuple[Popen, Popen, Optional[Popen]]:
    """Start RabbitMQ, Redis and Celery isntances.

    sttgs must be imported here because otherwise it may cause some problems
    """
    from app.config import sttgs

    # Start postgres server
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

    if celery_worker:
        # Start celery worker
        celery_worker_process = start_celery_worker(debug=debug_celery_worker)
    else:
        celery_worker_process = None

    return rabbitmq_server_process, redis_server_process, celery_worker_process


def teardown_services(
    rabbitmq_server_process: Popen,
    redis_server_process: Popen,
    celery_worker_process: Optional[Popen] = None,
    postgres_datadir: str = '/usr/local/var/postgres',
) -> None:
    if celery_worker_process is not None:
        celery_worker_process.terminate()
    rabbitmq_server_teardown(rabbitmq_server_process)
    redis_server_teardown(redis_server_process)
    postgres_server_teardown(postgres_datadir)

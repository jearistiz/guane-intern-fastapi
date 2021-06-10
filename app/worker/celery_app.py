from celery import Celery

from app.config import sttgs


celery_app = Celery(
    'celery_worker',
    broker=sttgs['RABBITMQ_URI'],
    backend=sttgs['CELERY_BAKCEND_URI'],
)

celery_app.autodiscover_tasks(['app.worker'])

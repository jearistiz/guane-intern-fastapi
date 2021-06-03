from .dogs import dogs_router
from .users import users_router
from .upload_file import upload_file_router
from .security import security_router
from .tasks import tasks_router


__all__ = [
    'dogs_router',
    'users_router',
    'upload_file_router',
    'security_router',
    'tasks_router',
]

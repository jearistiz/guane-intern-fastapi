from typing import Any, Optional
from pydantic import BaseModel


class CeleryTaskResponse(BaseModel):
    task_complexity: int
    status: str = 'Successfully submitted the task.'
    server_message: Optional[Any]
    success: bool = True

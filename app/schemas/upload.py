from typing import Optional

from pydantic import BaseModel


class UploadFileStatus(BaseModel):
    success: bool
    remote_server_response: Optional[dict]
    remote_server_status_code: Optional[int]
    message: Optional[str]

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request

from app import schemas
from app.config import sttgs
from app.services.http_request import post_file_to_uri
from app.services.paths import join_relative_path


upload_file_router = APIRouter()


@upload_file_router.post(
    '/file-to-guane',
    response_model=schemas.UploadFileStatus
)
async def post_file_to_guane(client_req: Request) -> Any:
    """With an empy body request to this endpoint, the api sends a a locally
    stored file to a previously defined endpoint (in this case, guane's test
    api).
    """
    this_file_path = Path(__file__).parent.absolute()
    upload_file_path = join_relative_path(
        this_file_path,
        sttgs.get('UPLOAD_FILE_PATH')
    )
    upload_req = post_file_to_uri(
        upload_file_path,
        message='Hello, guane. This is Juan Esteban Aristizabal!'
    )
    return {
        'success': True if upload_req.status_code == 201 else False,
        'remote_server_response': upload_req.json(),
        'remote_server_status_code': upload_req.status_code
    }

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
import requests as req

from app import schemas
from app.config import sttgs
from app.crud import superuser_crud
from app.utils.http_request import post_file_to_uri
from app.utils.paths import join_relative_path


upload_file_router = APIRouter()


@upload_file_router.post(
    '/file-to-guane',
    response_model=schemas.UploadFileStatus,
    status_code=status.HTTP_201_CREATED,
)
async def post_file_to_guane(
    client_req: Request,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
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

    # If timeout in upload_request
    if not isinstance(upload_req, req.Response):
        if upload_req:
            raise HTTPException(
                502,
                detail={
                    'success': False,
                    'remote_server_response': None,
                    'remote_server_status_code': None,
                    'message': upload_req
                }
            )
        else:
            raise HTTPException(502)

    return {
        'success': True if upload_req.status_code == 201 else False,
        'remote_server_response': upload_req.json(),
        'remote_server_status_code': upload_req.status_code
    }

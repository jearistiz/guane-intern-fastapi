import os
from shutil import copyfileobj
from typing import Optional
from pathlib import Path


import requests as req

from app.config import sttgs


def get_dog_picture_uri(
    api_uri: Optional[str] = sttgs.get('DOG_API_URI')
) -> Optional[str]:
    """Returns None if an exception occurs.
    """
    if api_uri:

        try:
            r = req.get(api_uri)
        except Exception:
            return None

        data_json = r.json()

        if (not r.status_code == 200) or (not isinstance(data_json, dict)):
            return None

        if data_json.get('status') == 'success':
            return data_json.get('message')

    return None


def post_file_to_uri(
    upload_file_path: Path,
    uri: str = sttgs.get('UPLOAD_FILE_URI'),
    file_content: str = 'image/png',
    *,
    message: str
) -> req.Response:
    """Post a file to uri."""
    # if file does not exist, post a text file
    os.makedirs(upload_file_path.parent, exist_ok=True)
    if not os.path.isfile(upload_file_path):
        upload_file_path = upload_file_path.parent / 'hello_guane.txt'
        file_content = 'text/plain'
        message = 'Original file was replaced by api.'
        with open(upload_file_path, 'w') as save_file:
            save_file.write('Hello guane, this is Juan Esteban Aristizábal!')

    # Read file and upload it to uri it using requests library
    with open(upload_file_path, 'rb') as payload:
        files_to_upload = {
            'file': (
                upload_file_path.name,
                payload,
                file_content,
                {'message': message}
            )
        }
        request = req.post(
            uri,
            files=files_to_upload
        )

        # Save a copy of the file just to verify that the uploaded object was
        # correctly read
        save_file_copy_path = (
            upload_file_path.parent / ('2-' + upload_file_path.name)
        )
        with open(save_file_copy_path, 'wb') as save_file_copy:
            payload.seek(0)
            save_file_copy.seek(0)
            copyfileobj(payload, save_file_copy)
            save_file_copy.truncate()

    return request


example_dog_urls = [
    "https://images.dog.ceo/breeds/retriever-golden/nina.jpg",
    "https://images.dog.ceo/breeds/papillon/n02086910_1613.jpg",
    "https://images.dog.ceo/breeds/buhund-norwegian/hakon1.jpg",
    "https://images.dog.ceo/breeds/terrier-toy/n02087046_4409.jpg",
]

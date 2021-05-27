from typing import Optional

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

from datetime import datetime
from typing import Any, Dict


def parse_dog_dict(
    create_date: datetime,
    name: str,
    picture: str,
    is_adopted: bool,
    id_user: int,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """Dog info contained in a dictionary
    """
    return {
        'create_date': create_date,
        'name': name,
        'picture': picture,
        'is_adopted': is_adopted,
        'id_user': id_user,
    }


def parse_user_dict(
    create_date: datetime,
    name: str,
    last_name: str,
    email: str,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """User info contained in a dictionary
    """
    return {
        'create_date': create_date,
        'name': name,
        'last_name': last_name,
        'email': email,
    }

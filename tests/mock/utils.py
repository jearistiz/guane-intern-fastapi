from datetime import datetime
from typing import Any, Dict


def dog_dict(
    create_date: datetime,
    name: str,
    picture: str,
    is_adopted: bool,
    id_user: int,
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


def user_dict(
    create_date: datetime,
    name: str,
    last_name: str,
    email: str,
) -> Dict[str, Any]:
    """User info contained in a dictionary
    """
    return {
        'name': name,
        'last_name': last_name,
        'email': email,
        'create_date': create_date,
    }

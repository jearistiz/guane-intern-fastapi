from datetime import datetime


def create_dog_dict_entry(
    id: int,
    create_date: datetime,
    name: str,
    picture: str,
    is_adopted: bool,
    id_user: int,
):
    return {
        'id': id,
        'create_date': create_date,
        'name': name,
        'picture': picture,
        'is_adopted': is_adopted,
        'id_user': id_user,
    }


dogs_info = [
    (1, datetime.utcnow(), 'Guane', 'https://randomurl.com', False, None)
    (2, datetime.utcnow(), 'Is', 'https://randomurl.com', False, None)
    (3, datetime.utcnow(), 'Great', 'https://randomurl.com', True, 1)
    (4, datetime.utcnow(), 'Yeah!', 'https://randomurl.com', True, 2)
]

dogs = [create_dog_dict_entry(*dog_info) for dog_info in dogs_info]

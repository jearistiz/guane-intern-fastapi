from datetime import datetime

from app.schemas import DogInDBBase, UserInDBBase
from app.db.utils.parse_dicts import parse_dog_dict, parse_user_dict
from app.services.http_request import get_dog_picture_uri

# Random date
date = datetime(2021, 5, 27, 3, 54, 58, 217637)

dogs_info = [
    [date, 'Guane', get_dog_picture_uri(), False, None],
    [date, 'Thori', get_dog_picture_uri(), False, None],
    [date, 'CharlieBot', get_dog_picture_uri(), True, 1],
    [date, 'Fuelai', get_dog_picture_uri(), True, 2],
]

dogs_mock_dicts = [
    parse_dog_dict(*dog_info) for dog_info in dogs_info
]

adopted_dogs_dicts = [
    dog_info for dog_info in dogs_mock_dicts
    if dog_info.get('is_adopted', None)
]

dogs_mock = [
    DogInDBBase(**dog_dict) for dog_dict in dogs_mock_dicts
]

users_info = [
    [date, 'Guane1', 'Enterprises', 'info@guane.com.co'],
    [date, 'Guane2', 'CharlieBot', 'CharlieBot@guane.com.co'],
    [date, 'Guane3', 'Thori', 'Thori@guane.com.co'],
    [date, 'Guane4', 'Fuelai', 'Fuelai@guane.com.co'],
]

users_mock_dicts = [
    parse_user_dict(*user_info) for user_info in users_info
]

users_mock = [
    UserInDBBase(**user_dict) for user_dict in users_mock_dicts
]

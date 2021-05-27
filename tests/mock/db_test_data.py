from datetime import datetime

from app.schemas import DogInDBBase, UserInDBBase
from .utils import parse_dog_dict, parse_user_dict


dogs_info = [
    [datetime.utcnow(), 'Guane', 'https://randomurl.com', False, None],
    [datetime.utcnow(), 'Is', 'https://randomurl.com', False, None],
    [datetime.utcnow(), 'Great', 'https://randomurl.com', True, 1],
    [datetime.utcnow(), 'Yeah!', 'https://randomurl.com', True, 2],
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
    [datetime.utcnow(), 'Guane1', 'Enterprises', 'info@guane.com.co'],
    [datetime.utcnow(), 'Guane2', 'CharlieBot', 'CharlieBot@guane.com.co'],
    [datetime.utcnow(), 'Guane3', 'Thori', 'Thori@guane.com.co'],
    [datetime.utcnow(), 'Guane4', 'Fuelai', 'Fuelai@guane.com.co'],
]

users_mock_dicts = [
    parse_user_dict(*user_info) for user_info in users_info
]

users_mock = [
    UserInDBBase(**user_dict) for user_dict in users_mock_dicts
]

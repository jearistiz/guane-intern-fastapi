from datetime import datetime

from app.schemas import DogInDBBase, UserInDBBase
from .utils import dog_dict, user_dict

dogs_info = [
    (datetime.utcnow(), 'Guane', 'https://randomurl.com', False, None),
    (datetime.utcnow(), 'Is', 'https://randomurl.com', False, None),
    (datetime.utcnow(), 'Great', 'https://randomurl.com', True, 1),
    (datetime.utcnow(), 'Yeah!', 'https://randomurl.com', True, 2),
]

dogs_mock = [
    DogInDBBase(**dog_dict(*dog_info)) for dog_info in dogs_info
]

users_info = [
    (datetime.utcnow(), 'Guane', 'Enterprises', 'info@guane.com.co'),
    (datetime.utcnow(), 'Guane', 'CharlieBot', 'CharlieBot@guane.com.co'),
    (datetime.utcnow(), 'Guane', 'Thori', 'Thori@guane.com.co'),
    (datetime.utcnow(), 'Guane', 'Fuelai', 'Fuelai@guane.com.co'),
]

users_mock = [
    UserInDBBase(**user_dict(*user_info)) for user_info in users_info
]

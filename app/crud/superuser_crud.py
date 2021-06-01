from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.config import sttgs
from app.schemas import TokenData, SuperUser, SuperUserInDB
from app.core.security.security import oauth2_scheme, auth_header
from app.db.data.superusers_fake_db import superusers_db


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return SuperUserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers=auth_header,
    )
    try:
        payload = jwt.decode(
            token,
            sttgs.get('SECRET_KEY'),
            algorithms=[sttgs.get('ALGORITHM')]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(superusers_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: SuperUser = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

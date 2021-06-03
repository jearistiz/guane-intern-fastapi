from typing import Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.config import sttgs
from app.core.security.pwd import authenticate_user
from app.core.security.security import auth_header
from app.core.security.token import create_access_token
from app.db.data.superusers_fake_db import superusers_db


security_router = APIRouter()


@security_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(  # noqa
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Try to get the token with one of this two superusers:

    user: guane
    password: ilovethori

    or

    user: juanes
    password: ilovecharliebot
    """
    user = authenticate_user(
        superusers_db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers=auth_header,
        )
    access_token_expires = timedelta(
        minutes=int(sttgs.get('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

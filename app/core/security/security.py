from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.config import sttgs


# Defines the authentication schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=sttgs.get('TOKEN_URI'))

# Handles the passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OpenAPI authentication header spec
auth_header = {"WWW-Authenticate": "Bearer"}

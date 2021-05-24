from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import sttgs, dog_api_prefix, user_api_prefix
from app.router import dog_router, user_router


app = FastAPI(title=sttgs.get('PROJECT_TITLE'))

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=sttgs.get('ALLOWED_HOSTS', ['*']).split(',')
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=sttgs.get('ALLOWED_ORIGINS', ['*']).split(','),
    allow_methods=sttgs.get('ALLOWED_METHODS', ['*']).split(','),
    allow_headers=sttgs.get('ALLOWED_HEADERS', ['*']).split(',')
)

app.include_router(dog_router, prefix=dog_api_prefix)
app.include_router(user_router, prefix=user_api_prefix)

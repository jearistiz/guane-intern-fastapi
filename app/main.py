from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import sttgs
from app.api.api import api_router


# Main app
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

app.include_router(api_router, prefix='/api')

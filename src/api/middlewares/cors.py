from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings


class ConfiguredCORSMiddleware(CORSMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(
            app=app,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS,
        )

from fastapi import FastAPI
from fastapi.requests import Request

from src.api.utils import APIUtils
from src.core.exceptions import CustomError


class ExceptionHandler:

    @classmethod
    def register(cls, app: FastAPI) -> None:
        @app.exception_handler(Exception)
        async def custom_exception_handler(request: Request, exc: Exception) -> None:  # noqa
            return APIUtils.unify(data=None, msg='error', code=500)

        @app.exception_handler(CustomError)
        async def custom_exception_handler(request: Request, exc: CustomError) -> None:  # noqa
            return APIUtils.unify(data=None, msg=exc.MSG, code=exc.STATUS_CODE)

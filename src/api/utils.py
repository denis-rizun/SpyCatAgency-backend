from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from src.infra.schemas.base import ResponseSchema


class APIUtils:

    @staticmethod
    def unify(data: BaseModel | None, code: int = HTTP_200_OK, msg: str = 'ok') -> ResponseSchema:
        content = ResponseSchema(statusCode=code, message=msg, data=data).model_dump()
        return JSONResponse(content=content, status_code=code)

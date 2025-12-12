from typing import Generic, TypeVar

from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class ResponseSchema(BaseModel, Generic[SchemaType]):
    statusCode: int
    message: str | None
    data: SchemaType | list[SchemaType] | None

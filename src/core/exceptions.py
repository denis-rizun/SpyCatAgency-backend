from starlette import status


class CustomError(Exception):
    MSG: str
    STATUS_CODE: int

    def __init__(self, msg: str | None = None) -> None:
        if msg:
            self.MSG = msg
        super().__init__(self.MSG)


class DatabaseError(CustomError):
    MSG = 'Database error'
    STATUS_CODE = status.HTTP_400_BAD_REQUEST


class DatabaseNotFoundError(DatabaseError):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class DatabaseDuplicationError(DatabaseError):
    STATUS_CODE = status.HTTP_409_CONFLICT


class InvalidBreedError(CustomError):
    MSG = 'Invalid breed'
    STATUS_CODE = status.HTTP_400_BAD_REQUEST


class CatHasActiveMissionError(CustomError):
    MSG = 'Cat has active mission'
    STATUS_CODE = status.HTTP_403_FORBIDDEN


class InvalidTargetsCountError(CustomError):
    MSG = 'Invalid breed'
    STATUS_CODE = status.HTTP_400_BAD_REQUEST


class EntityCompletedError(CustomError):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    
class EntityAssignedError(CustomError):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
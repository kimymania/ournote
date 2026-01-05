from starlette import status
from starlette.exceptions import HTTPException


class AuthenticationError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail if detail is not None else "Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail if detail is not None else "You are not authorized",
        )


class DuplicateDataError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="data already exists in DB",
        )


class NotFoundError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail if detail is not None else "Content Not Found",
        )


class DBError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail if detail is not None else "Failed to perform database operation",
        )

from fastapi import HTTPException, status

class RugbyFantasyException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(RugbyFantasyException):
    def __init__(self, resource: str, id: int):
        super().__init__(f"{resource} with id {id} not found", status.HTTP_404_NOT_FOUND)

class ValidationError(RugbyFantasyException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)

class UnauthorizedError(RugbyFantasyException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)
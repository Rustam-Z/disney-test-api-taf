from typing import Optional
from pydantic import BaseModel, validator, StrictStr, StrictBool


class Response(BaseModel):
    status: StrictBool
    message: StrictStr
    data: Optional[None] = None
    error: Optional[None] = None


class SuccessResponse(Response):
    @validator('status')
    def check_status(cls, value):
        if value is not True:
            raise ValueError('status must be True')
        return value


class ErrorResponse(Response):
    @validator('status')
    def check_status(cls, value):
        if value is True:
            raise ValueError('status must be False')
        return value

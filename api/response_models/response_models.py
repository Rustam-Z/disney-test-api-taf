from typing import Optional, Dict

from pydantic import BaseModel, validator, StrictStr, StrictBool


class _Response(BaseModel):
    status: StrictBool
    message: StrictStr  # message field is expected to be different for different response_models.
    data: Optional[None] = None
    error: Optional[None] = None


class SuccessResponse(_Response):
    data: Dict

    @validator('status')
    def check_status(cls, value):
        if value is not True:
            raise ValueError('status must be True')
        return value

    # TODO: messages are not validated yet.
    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


class ErrorResponse(_Response):
    error: Dict

    @validator('status')
    def check_status(cls, value):
        if value is True:
            raise ValueError('status must be False')
        return value

    # TODO: messages are not validated yet.
    @validator('message')
    def check_message(cls, value):
        expected_message = 'Error'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value

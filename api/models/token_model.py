from pydantic import BaseModel, validator, StrictStr, StrictInt, StrictBool

from api.models.response_model import SuccessResponse, ErrorResponse


class _DataField(BaseModel):
    refresh: StrictStr
    access: StrictStr
    id: StrictInt
    is_superuser: StrictBool


class _ErrorField(BaseModel):
    detail: StrictStr


class TokenSuccessResponse(SuccessResponse):
    data: _DataField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


class TokenErrorResponse(ErrorResponse):
    error: _ErrorField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Error'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value

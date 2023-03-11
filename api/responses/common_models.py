"""
Common response models.

Example usage:
    data = {
        "status": False,
        "message": "Error",
        "data": None,
        "error": {
            "detail": "Authentication credentials were not provided."
        }
    }
    model = AuthErrorResponse(**data)

"""
from pydantic import validator

from api.responses.response_models import ErrorResponse


class AuthErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = 'Authentication credentials were not provided.'

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')


class UnauthRequestErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('message')
        expected_message = "'AnonymousUser' object has no attribute 'role'"

        if detail == expected_message:
            return value

        raise ValueError('error should include message key')

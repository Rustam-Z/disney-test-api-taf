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

from api.enums.errors import ErrorDetail
from api.response_models.response_models import ErrorResponse


class InvalidTokenErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = ErrorDetail.TOKEN_IS_INVALID.value

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')


class AuthErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = ErrorDetail.AUTH_CREDS_NOT_PROVIDED.value

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')


class NoPermissionErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = ErrorDetail.NO_PERMISSION.value

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')


class OnlySuperuserCanPerformErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = ErrorDetail.ONLY_SUPERUSER.value

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')


class RequestWithoutSectionParamErrorResponse(ErrorResponse):
    @validator('error')
    def check_message(cls, value):
        """
        Validate that the value in the "detail" key == expected_message.
        """
        detail = value.get('detail')
        expected_message = ErrorDetail.NO_SUCH_MENU.value

        if detail == expected_message:
            return value

        raise ValueError('error should include detail key')

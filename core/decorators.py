import pytest

from core.enums.users import User


def users(*args):
    """
    This decorator is used to authorize tests using parametrization.
    If @users decorator is used, you have to add `user` parameter too for test function.

    Usage example (two lines below are identical):
        @pytest.mark.parametrize('user', [User.SUPERUSER, User.FACILITY_ADMIN])
        @users(User.SUPERUSER, User.FACILITY_ADMIN)

    """

    def deco(for_deco):
        if not args:
            raise TypeError("Please provide at least 1 user type in arguments.")

        params = []
        for user_type in args:
            if not isinstance(user_type, User):
                raise TypeError('Please use User enum values in args.')
            params.append(user_type)

        dec_var = pytest.mark.parametrize('user', params)

        return dec_var(for_deco)

    return deco


def mobile():
    """
    Creates the parametrized mark for test.

    Two examples below are the same:
        @pytest.mark.parametrize('is_for_mobile', [False, True])
        @is_for_mobile()

    """
    def deco(for_deco):
        dec_var = pytest.mark.parametrize('is_for_mobile', [False, True])
        return dec_var(for_deco)

    return deco

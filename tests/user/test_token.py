"""
Tests for user authentication, access token and refresh token.
"""

import pytest

from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from api.requests.token_api import TokenAPI
from core.config.users import get_random_user
from core.enums.users import User
from core.helpers.jwt_helper import decode_jwt
import data


class TestLogin:
    @pytest.mark.parametrize('user_type', [User.FACILITY_ADMIN, User.SUPERUSER])
    @users(User.NONE)
    def test_loginUser_withValidCredentials_returns200AndTokens(self, client, user, user_type):
        """
        GIVEN valid email and valid password,
        WHEN POST /user/token/ request is executed,
        THEN response code should be 200,
        AND response body contains access and refresh tokens.
        """
        # Arrange
        email, password = get_random_user(user_type)

        # Act
        response, model = TokenAPI(client).login(email=email, password=password)

        # Assert
        APIResponse(response).assert_status(200)

        if user_type == User.SUPERUSER:
            assert model.data.is_superuser is True, '`is_superuser` should be True for superuser.'

        access_jwt_data = decode_jwt(model.data.access)
        assert access_jwt_data.get('user_id') == model.data.id, 'User IDs are not matching.'
        assert access_jwt_data.get('token_type') == 'access'

        refresh_jwt_data = decode_jwt(model.data.refresh)
        assert refresh_jwt_data.get('user_id') == model.data.id, 'User IDs are not matching.'
        assert refresh_jwt_data.get('token_type') == 'refresh'

    @pytest.mark.parametrize('user_type', [User.FACILITY_ADMIN])
    @users(User.NONE)
    def test_loginUser_withValidEmailAndWrongPassword_returns401AndError(self, client, user, user_type):
        """
        GIVEN valid email and valid password,
        WHEN POST /user/token/ request is executed,
        THEN response code should be 200,
        AND response body contains access and refresh tokens.
        """
        # Arrange
        email, password = get_random_user(user_type)
        password = data.fake.password()

        # Act
        response, model = TokenAPI(client).login(email=email, password=password)

        # Assert
        APIResponse(response).assert_status(401)

    @pytest.mark.parametrize('email, password', [
        (data.fake.email(), data.fake.password()),
        (data.fake.name(), data.fake.password()),  # Wrong email format.
    ])
    @users(User.NONE)
    def test_loginUser_withWrongEmailAndWrongPassword_returns401AndError(self, client, user, email, password):
        response, model = TokenAPI(client).login(email=email, password=password)
        APIResponse(response).assert_status(401)
        assert model.error.get('detail') == ErrorDetail.WRONG_CREDENTIALS.value

    @pytest.mark.parametrize('email, password, error', [
        (' ', data.fake.password(), {"email": [ErrorDetail.FIELD_MAY_NOT_BE_BLANK.value]}),
        (data.fake.password(), ' ', {"password": [ErrorDetail.FIELD_MAY_NOT_BE_BLANK.value]}),
        (' ', ' ', {"email": [ErrorDetail.FIELD_MAY_NOT_BE_BLANK.value],
                    "password": [ErrorDetail.FIELD_MAY_NOT_BE_BLANK.value]}),
    ])
    @users(User.NONE)
    def test_loginUser_withEmptyFields_returns400AndError(self, client, user, email, password, error):
        response, model = TokenAPI(client).login(email=email, password=password)
        APIResponse(response).assert_status(400)
        assert model.error == error


class TestRefreshToken:
    @pytest.mark.parametrize('user_type', [User.FACILITY_ADMIN, User.SUPERUSER])
    @users(User.NONE)
    def test_getNewAccessToken_withValidRefreshToken_returns200AndTokens(self, client, user, user_type):
        # Arrange
        email, password = get_random_user(user_type)
        response, model = TokenAPI(client).login(email=email, password=password)
        refresh_token = model.data.refresh

        # Act
        response, model = TokenAPI(client).refresh_token(refresh=refresh_token)
        old_refresh_jwt_data = decode_jwt(refresh_token)
        new_access_jwt_data = decode_jwt(model.data.access)
        new_refresh_jwt_data = decode_jwt(model.data.refresh)

        # Assert
        APIResponse(response).assert_status(200)
        assert old_refresh_jwt_data.get('user_id') == \
               new_access_jwt_data.get('user_id') == \
               new_refresh_jwt_data.get('user_id')

    @users(User.NONE)
    def test_getNewAccessToken_withWrongRefreshToken_returns401AndError(self, client, user):
        # Arrange
        refresh_token = data.fake.jwt_token()

        # Act
        response, model = TokenAPI(client).refresh_token(refresh=refresh_token)

        # Assert
        APIResponse(response).assert_status(401)
        assert model.error.get('detail') == 'Token is invalid or expired'  # TODO: message should end with dot.

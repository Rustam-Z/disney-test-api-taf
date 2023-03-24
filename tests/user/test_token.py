"""
Test user authentication. Access token and refresh token.
"""
import pytest

from core.api_response import APIResponse
from core.decorators import users
from core.http_client import HTTPClient
from api.requests.token_api import TokenAPI
from core.config.users import get_random_user
from core.enums.users import User
from core.helpers.jwt_helper import decode_jwt
import data


class TestToken:
    @users(User.NONE)
    def test_superUserValidEmailAndValidPassword_returnsToken(self, client, user):
        """
        GIVEN valid email and valid password,
        WHEN POST request is executed,
        THEN response code = 200,
        AND response body contains access and refresh tokens.
        """
        email, password = get_random_user(User.SUPERUSER)
        response, model = TokenAPI(client).login(email=email, password=password)  # Send request.

        APIResponse(response).check_status(200)
        assert model.data.is_superuser is True, '`is_superuser` should be True for superuser'

        access_jwt_data = decode_jwt(model.data.access)
        assert access_jwt_data.get('user_id') == model.data.id, 'ids are not matching in access token and response id'
        assert access_jwt_data.get('token_type') == 'access'

        refresh_jwt_data = decode_jwt(model.data.refresh)
        assert refresh_jwt_data.get('user_id') == model.data.id, 'ids are not matching in refresh token and response id'
        assert refresh_jwt_data.get('token_type') == 'refresh'

    @users(User.NONE)
    def test_validEmailAndWrongPassword_returnsError(self, client, user):
        """
        GIVEN valid email and valid password,
        WHEN POST request is executed,
        THEN response code = 200,
        AND response body contains access and refresh tokens.
        """
        email, password = get_random_user(User.SUPERUSER)
        password = data.fake.password()

        response, model = TokenAPI(client).login(email=email, password=password)
        APIResponse(response).check_status(401)

    @pytest.mark.parametrize('email, password', [
        (data.fake.email(), data.fake.password()),
        (data.fake.name(), data.fake.password()),  # Wrong email format.
    ])
    @users(User.NONE)
    def test_wrongEmailAndWrongPassword_returnsError(self, client, user, email, password):
        response, model = TokenAPI(client).login(email=email, password=password)

        APIResponse(response).check_status(401)
        assert model.error.get('detail') == 'No active account found with the given credentials'

    @pytest.mark.parametrize('email, password, error', [
        (' ', data.fake.password(), {"email": ["This field may not be blank."]}),
        (data.fake.password(), ' ', {"password": ["This field may not be blank."]}),
        (' ', ' ', {"email": ["This field may not be blank."], "password": ["This field may not be blank."]}),
    ])
    @users(User.NONE)
    def test_emptyFields_returnsError(self, client, user, email, password, error):
        response, model = TokenAPI(client).login(email=email, password=password)

        APIResponse(response).check_status(400)
        assert model.error == error, 'Error content is not matching.'


class TestRefreshToken:
    @staticmethod
    def get_refresh_token(client: HTTPClient) -> str:
        email, password = get_random_user(User.SUPERUSER)
        response, model = TokenAPI(client).login(email=email, password=password)
        return model.data.refresh

    @users(User.NONE)
    def test_validRefreshToken_returnsToken(self, client, user):
        refresh_token = self.get_refresh_token(client)
        response, model = TokenAPI(client).refresh_token(refresh=refresh_token)

        APIResponse(response).check_status(200)

        old_refresh_jwt_data = decode_jwt(refresh_token)
        new_access_jwt_data = decode_jwt(model.data.access)
        new_refresh_jwt_data = decode_jwt(model.data.refresh)
        assert old_refresh_jwt_data.get('user_id') == \
               new_access_jwt_data.get('user_id') == \
               new_refresh_jwt_data.get('user_id')

    @users(User.NONE)
    def test_wrongRefreshToken_returnsError(self, client, user):
        refresh_token = data.fake.jwt_token()
        response, model = TokenAPI(client).refresh_token(refresh=refresh_token)

        APIResponse(response).check_status(401)
        assert model.error.get('detail') == 'Token is invalid or expired'

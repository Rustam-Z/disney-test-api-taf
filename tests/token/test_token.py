"""
Test user authentication. Access token and refresh token.
"""
import pytest
from faker import Faker

from api.api_response import APIResponse
from api.requests.token_api import TokenAPI
from api.responses.token_model import TokenErrorResponse
from core.config.users import get_random_user
from core.enums.auth import Auth
from core.helpers.jwt_helpers import decode_jwt


class TestToken:
    def test_superUserValidEmailAndValidPassword_returnsToken(self, client):
        """
        GIVEN valid email and valid password,
        WHEN POST request is executed,
        THEN response code = 200,
        AND response body contains access and refresh tokens.
        """
        email, password = get_random_user(Auth.SUPERUSER)
        response, model = TokenAPI(client).login(email=email, password=password)  # Send request.

        APIResponse(response).check_status(200)
        assert model.data.is_superuser is True, '`is_superuser` should be True for superuser'

        access_jwt_data = decode_jwt(model.data.access)
        assert access_jwt_data.get('user_id') == model.data.id, 'ids are not matching in access token and response id'
        assert access_jwt_data.get('token_type') == 'access'

        refresh_jwt_data = decode_jwt(model.data.refresh)
        assert refresh_jwt_data.get('user_id') == model.data.id, 'ids are not matching in refresh token and response id'
        assert refresh_jwt_data.get('token_type') == 'refresh'

    def test_validEmailAndWrongPassword_returnsError(self, client):
        """
        GIVEN valid email and valid password,
        WHEN POST request is executed,
        THEN response code = 200,
        AND response body contains access and refresh tokens.
        """
        email, password = get_random_user(Auth.SUPERUSER)
        password = Faker().password()

        response, model = TokenAPI(client).login(email=email, password=password)
        APIResponse(response).check_status(401)

    @pytest.mark.parametrize('email, password', [
        (Faker().email(), Faker().password()),
        (Faker().name(), Faker().password()),  # Wrong email format.
    ])
    def test_wrongEmailAndWrongPassword_returnsError(self, client, email, password):
        response, model = TokenAPI(client).login(email=email, password=password)

        APIResponse(response).check_status(401)
        assert model.error.get('detail') == 'No active account found with the given credentials'

    @pytest.mark.parametrize('email, password, error', [
        (' ', Faker().password(), {"email": ["This field may not be blank."]}),
        (Faker().password(), ' ', {"password": ["This field may not be blank."]}),
        (' ', ' ', {"email": ["This field may not be blank."], "password": ["This field may not be blank."]}),
    ])
    def test_emptyFields_returnsError(self, client, email, password, error):
        response, model = TokenAPI(client).login(email=email, password=password)

        APIResponse(response).check_status(400)
        assert model.error == error, 'Error content is not matching.'

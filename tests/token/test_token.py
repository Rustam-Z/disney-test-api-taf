"""
Test user authentication. Access token and refresh token.
"""
from api.requests.token_api import TokenAPI
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
        model = TokenAPI(client).login(email=email, password=password)  # Send request.

        assert model.data.is_superuser is True, '`is_superuser` should be True for superuser'

        access_jwt_data = decode_jwt(model.data.access)
        assert access_jwt_data.get('user_id') == model.data.id, 'ids are not matching in access token and response id'
        assert access_jwt_data.get('token_type') == 'access'

        refresh_jwt_data = decode_jwt(model.data.refresh)
        assert refresh_jwt_data.get('user_id') == model.data.id, 'ids are not matching in refresh token and response id'
        assert refresh_jwt_data.get('token_type') == 'refresh'

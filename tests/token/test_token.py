"""
Test user authentication. Access token and refresh token.
"""

from core.config.users import get_random_user
from core.enums.auth import Auth
from api.api_response import APIResponse


class TestToken:
    def test_superUserValidEmailAndValidPassword_returnsToken(self, client):
        """
        GIVEN valid email and valid password,
        WHEN POST request is executed,
        THEN response code = 200,
        AND response body contains access and refresh tokens.
        """
        email, password = get_random_user(Auth.SUPERUSER)
        payload = {
            'email': email,
            'password': password
        }
        response = client.post('/user/token/', data=payload)
        APIResponse(response).check_status(200)

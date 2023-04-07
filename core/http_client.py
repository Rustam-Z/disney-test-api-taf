import requests
from requests import Response


class HTTPClient:
    _VALID_HTTP_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    _DEFAULT_HTTP_HEADERS = {
        'Content-Type': 'application/json',
        'accept': '*/*',
    }

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        # Set up initial headers.
        self.remove_all_headers()
        self.update_headers(self._DEFAULT_HTTP_HEADERS)

    def send_request(self, method: str, path: str, **kwargs) -> Response:
        if method not in self._VALID_HTTP_METHODS:
            raise ValueError(f'Invalid HTTP method "{method}"')

        url = self.build_url(self.base_url, path)
        response = self.session.request(method, url, **kwargs)
        return response

    def get(self, path: str, params: dict = None, headers: dict = None) -> Response:
        url = self.build_url(self.base_url, path)
        response = self.session.get(url, params=params, headers=headers)
        return response

    def post(self, path: str, data: dict = None, params: dict = None, headers: dict = None) -> Response:
        url = self.build_url(self.base_url, path)
        response = self.session.post(url, json=data, params=params, headers=headers)
        return response

    def patch(self, path: str, data: dict = None, params: dict = None, headers: dict = None) -> Response:
        url = self.build_url(self.base_url, path)
        response = self.session.patch(url, json=data, params=params, headers=headers)
        return response

    def delete(self, path: str, params: dict = None, headers: dict = None) -> Response:
        url = self.build_url(self.base_url, path)
        response = self.session.delete(url, params=params, headers=headers)
        return response

    def update_headers(self, headers: dict) -> None:
        """Updates HTTP request headers.

        Args:
            headers: Dictionary, headers and values.

        Returns:
            None
        """
        self.session.headers.update(headers)

    def remove_headers(self, *headers) -> None:
        """Removes HTTP headers. Just pass headers name as arguments which calling this method.

        Example usage:
            self.remove_headers('Authorization', 'website')

        Args:
            *headers: Headers names as positional argument.

        Returns:
            None
        """
        for header in headers:
            self.session.headers.pop(header, None)

    def remove_all_headers(self) -> None:
        """Removes all HTTP headers from request.

        Returns:
            None
        """
        self.session.headers = {}

    @staticmethod
    def build_url(base_url: str, path: str, protocol: str = 'https') -> str:
        """Build the full URL, handling trailing/leading slashes and allowing specification of the protocol.

        Args:
            base_url: The API host URL, and any other info like API version. Example: test.com/api/v1
            path: The path to resource. Example: /path/1/version/2
            protocol: Data transfer protocols HTTPS, HTTP, FTP, TCP, etc.

        Returns:

        """
        if base_url.endswith('/'):
            base_url = base_url[:-1]  # Remove trailing slash.
        if not path.startswith('/'):
            path = '/' + path  # Add leading slash.
        if not path.endswith('/'):
            path = path + '/'
        return f"{protocol}://{base_url}{path}"

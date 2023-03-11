import requests
from requests import Response


class HTTPClient:
    VALID_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        # Set up initial headers.
        headers = {
            'Content-Type': 'application/json',
        }
        self.remove_all_headers()
        self.update_headers(headers)

    def send_request(self, method: str, path: str, **kwargs) -> Response:
        if method not in self.VALID_METHODS:
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
        # Needed for authentication purposes
        self.session.headers.update(headers)

    def remove_headers(self, *headers) -> None:
        for header in headers:
            try:
                del self.session.headers[header]
            except KeyError:
                print(f'{header}: header does\'s exist.')  # Only for debugging purposes.

    def remove_all_headers(self) -> None:
        self.session.headers = {}

    @staticmethod
    def build_url(base_url: str, path: str) -> str:
        """
        Should build the full path, handle / (slash).
        The path should end with /.
        """
        base_url = base_url[:-1] if base_url.endswith('/') else base_url
        path = '/' + path if not path.startswith('/') else path
        path += '/' if not path.endswith('/') else ''
        return base_url + path

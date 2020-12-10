from datetime import datetime
from json import loads
from os import getenv
from typing import NamedTuple

import requests

DEFAULT_NET_DELAY = 20


class ApiError(TypeError):
    def __init__(self, *args):
        super().__init__(*args)


class FlaskAPIToken(NamedTuple):
    token: str
    expired: datetime


class FlaskAPI:
    username: str
    password: str
    base_url: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = 'https://demo-api.flaskdata.io'

    def authorize(self) -> FlaskAPIToken:
        full_url = f'{self.base_url}/auth/authorize'
        data = {
            "email": self.username,
            "password": self.password
        }
        res = requests.post(full_url, json=data, timeout=DEFAULT_NET_DELAY)
        if res.status_code == 200:
            text = res.text
            json = loads(text)
            expired = datetime.strptime(json['expired'], '%Y-%m-%dT%H:%M:%S.%fZ')
            return FlaskAPIToken(json['token'], expired)
        else:
            raise ApiError('Invalid api response')


class FlaskAPIIDP(FlaskAPI):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.base_url = 'https://demo-idp.flaskdata.io'

    def authorize(self):
        full_url = f'{self.base_url}/auth/mobile-form-authorization'
        data = {
            "email": self.username,
            "password": self.password
        }
        res = requests.post(full_url, json=data, timeout=DEFAULT_NET_DELAY)
        if res.status_code == 200:
            pass
        else:
            raise ApiError(f'Invalid api response ({res.status_code}): {res.text}')


FLASK_API_USER = getenv('FLASK_API_USER')
FLASK_API_PASSWORD = getenv('FLASK_API_PASSWORD')
FLASK_API_IDP_USER = getenv('FLASK_API_IDP_USER')
FLASK_API_IDP_PASSWORD = getenv('FLASK_API_IDP_PASSWORD')


def main():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    api_idp = FlaskAPIIDP(FLASK_API_IDP_USER, FLASK_API_IDP_PASSWORD)

    # 1
    api.authorize()
    api_idp.authorize()


if __name__ == '__main__':
    main()

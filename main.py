from datetime import datetime
from json import loads
from os import getenv
from typing import List, NamedTuple

import requests

DEFAULT_NET_DELAY = 20


class ApiError(TypeError):
    def __init__(self, *args):
        super().__init__(*args)


class FlaskAPIToken(NamedTuple):
    token: str
    expired: datetime


class FlaskAPIIDPSelf(NamedTuple):
    item_id: int
    first_name: str
    last_name: str
    edc_username: str
    email: str
    finished_tutorial: bool
    company_name: str
    study_subject_label: str
    customer_id: int
    phone: str


class FlaskAPISubjectStudies(NamedTuple):
    study_id: int
    brief_title: str
    unique_protocolid: str
    official_title: str
    status_id: int
    status: str
    study_status_id: int


class FlaskAPI:
    username: str
    password: str
    base_url: str

    def __init__(self, username: str, password: str, base_url='https://demo-api.flaskdata.io'):
        self.username = username
        self.password = password
        self.base_url = base_url

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
            raise ApiError(f'Invalid api response ({res.status_code}): {res.text}')

    def subject_studies(self, token: str, subject_id: int) -> List[FlaskAPISubjectStudies]:
        full_url = f'{self.base_url}/flask/study/subject-studies'
        headers = {
            'Authorization': f'JWT {token}'  # or 'Bearer <ACCESS_TOKEN>'
        }
        data = {
            "subject_id": subject_id
        }
        res = requests.post(full_url, json=data, timeout=DEFAULT_NET_DELAY, headers=headers)
        if res.status_code == 200:
            text = res.text
            json = loads(text)
            result: List[FlaskAPISubjectStudies] = []
            for item in json:
                result.append(FlaskAPISubjectStudies(
                    item['study_id'],
                    item['brief_title'],
                    item['unique_protocolid'],
                    item['official_title'],
                    item['status_id'],
                    item['status'],
                    item['study_status_id'],
                ))
            return result
        else:
            raise ApiError(f'Invalid api response ({res.status_code}): {res.text}')

    def create_crf_and_insert_data(self, token):
        full_url = f'{self.base_url}/flask/crf/create-CRF-and-insert-data'
        headers = {
            'Authorization': f'JWT {token}'  # or 'Bearer <ACCESS_TOKEN>'
        }
        data = {
            "study_id": 3581600,
            "subject_label": "001-023",
            "event_name": "01-Screening",
            "crf_name": "Demographics",
            "crf_data": {
                "GENDER": "Female",
                "AGE": "21"
            }
        }
        res = requests.post(full_url, json=data, timeout=DEFAULT_NET_DELAY, headers=headers)
        if res.status_code == 200:
            return
        else:
            raise ApiError(f'Invalid api response ({res.status_code}): {res.text}')


class FlaskAPIIDP:
    username: str
    password: str
    base_url: str

    def __init__(self, username: str, password: str, base_url='https://demo-idp.flaskdata.io'):
        self.username = username
        self.password = password
        self.base_url = base_url

    def authorize(self, token: str) -> FlaskAPIToken:
        full_url = f'{self.base_url}/auth/mobile-form-authorization'
        data = {
            "email": self.username,
            "password": self.password
        }
        headers = {
            'Authorization': f'JWT {token}'  # or 'Bearer <ACCESS_TOKEN>'
        }
        res = requests.post(full_url, json=data, timeout=DEFAULT_NET_DELAY, headers=headers)
        if res.status_code == 200:
            text = res.text
            json = loads(text)
            expired = datetime.strptime(json['expired'], '%Y-%m-%dT%H:%M:%S.%fZ')
            return FlaskAPIToken(json['token'], expired)
        else:
            raise ApiError(f'Invalid api response ({res.status_code}): {res.text}')

    def get_self(self, token: str) -> FlaskAPIIDPSelf:
        headers = {
            'Authorization': f'JWT {token}'  # or 'Bearer <ACCESS_TOKEN>'
        }
        full_url = f'{self.base_url}/auth/self'
        res = requests.get(full_url, headers=headers, timeout=DEFAULT_NET_DELAY)
        if res.status_code == 200:
            text = res.text
            json = loads(text)
            return FlaskAPIIDPSelf(
                json['id'],
                json['first_name'],
                json['last_name'],
                json['edc_username'],
                json['email'],
                json['finished_tutorial'],
                json['company_name'],
                json['study_subject_label'],
                json['customer_id'],
                json['phone'],
            )
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
    api_token = api.authorize()
    api_idp_token = api_idp.authorize(api_token.token)

    # 2
    self_data = api_idp.get_self(api_idp_token.token)

    # 3
    api.subject_studies(api_idp_token.token, self_data.item_id)

    api.create_crf_and_insert_data(api_token.token)


if __name__ == '__main__':
    main()

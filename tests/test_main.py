from main import (FLASK_API_IDP_PASSWORD, FLASK_API_IDP_USER,
                  FLASK_API_PASSWORD, FLASK_API_USER, FlaskAPI, FlaskAPIIDP,
                  FlaskAPIIDPSelf, FlaskAPIToken)


def test_authorize():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    result = api.authorize()
    assert type(result) is FlaskAPIToken


def test_authorize_idp():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    api_token = api.authorize()
    api_idp = FlaskAPIIDP(FLASK_API_IDP_USER, FLASK_API_IDP_PASSWORD)
    result = api_idp.authorize(api_token.token)
    assert type(result) is FlaskAPIToken


def test_get_self_idp():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    api_token = api.authorize()
    api_idp = FlaskAPIIDP(FLASK_API_IDP_USER, FLASK_API_IDP_PASSWORD)
    api_idp_token = api_idp.authorize(api_token.token)
    self_data = api_idp.get_self(api_idp_token.token)
    assert type(self_data) is FlaskAPIIDPSelf


def test_studies():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    api_token = api.authorize()
    api_idp = FlaskAPIIDP(FLASK_API_IDP_USER, FLASK_API_IDP_PASSWORD)
    api_idp_token = api_idp.authorize(api_token.token)
    self_data = api_idp.get_self(api_idp_token.token)
    studies = api.subject_studies(api_idp_token.token, self_data.item_id)
    assert type(studies) is list
    assert len(studies) == 3
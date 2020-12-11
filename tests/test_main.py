from main import (FLASK_API_IDP_PASSWORD, FLASK_API_IDP_USER,
                  FLASK_API_PASSWORD, FLASK_API_USER, FlaskAPI, FlaskAPIIDP,
                  FlaskAPIToken)


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
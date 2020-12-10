from main import FLASK_API_PASSWORD, FLASK_API_USER, FlaskAPI, FlaskAPIToken


def test_authorize():
    api = FlaskAPI(FLASK_API_USER, FLASK_API_PASSWORD)
    result = api.authorize()
    assert type(result) is FlaskAPIToken

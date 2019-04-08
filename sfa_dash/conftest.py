import pytest


from sfa_dash import create_app
import requests


@pytest.fixture(scope='session')
def auth_token():
    token_req = requests.post(
        'https://solarforecastarbiter.auth0.com/oauth/token',
        headers={'content-type': 'application/json'},
        data=('{"grant_type": "password", '
              '"username": "testing@solarforecastarbiter.org",'
              '"password": "Thepassword123!", '
              '"audience": "https://api.solarforecastarbiter.org", '
              '"client_id": "c16EJo48lbTCQEhqSztGGlmxxxmZ4zX7"}'))
    if token_req.status_code != 200:
        pytest.skip('Cannot retrieve valid Auth0 token')
    else:
        token = token_req.json()['access_token']
        return token

@pytest.fixture()
def app():
    return create_app('sfa_dash.config.TestConfig')

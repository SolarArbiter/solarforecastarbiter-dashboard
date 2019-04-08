import pdb
import pytest
import flask
from flask import current_app, request
from flask_dance.consumer.storage import MemoryStorage


from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError


exp_oauth_token = {
    'auth0_oauth_token': {
        'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJpc3MiOiJodHRwczovL3NvbGFyZm9yZWNhc3RhcmJpdGVyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1YmUzNDNkZjcwMjU0MDYyMzc4MjBiODUiLCJhdWQiOlsiaHR0cHM6Ly9hcGkuc29sYXJmb3JlY2FzdGFyYml0ZXIub3JnIiwiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTU0NzU3MDQ2LCJleHAiOjE1NTQ3Njc4NDYsImF6cCI6IlByRTM5QWR0R01QSTRnSzJoUnZXWjJhRFJhcmZwZzdBIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCJ9.QR4syLZ_TlOhgexUYXsxLhYKwpASyMCGoHlywZ0dsdji2W8894rFqJgDMEvYFzHkNyUPPl2SO6iT2iGhli4RCZgmZq78fL_z4pu0m1eAv-SewY6N-LS8T2EZSoJuyk_imdjVyuwO5FV1t8yfrUt9_fEbD2HkzdFV0YtV6sAG2NfZf6fGGocsjx9JP2TyMpw50P3B7Q9KkXGhNf0bWkdashbXeu6jGza5uZ0dS7I9FhxluBBrC9aBwTJnPNZIpEJZwl6bQTkXnHl7QxZGxuC68ZEt06wVeMTUNDWrxsOTFvei3SIsNVswv6PqodqqsRhIcjJt4mToW48PHfeSzwHEFg', # NOQA
        'expires_at': 1554767846.445257,
        'expires_in': 10206.142375,
        'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJuaWNrbmFtZSI6InRlc3RpbmciLCJuYW1lIjoidGVzdGluZ0Bzb2xhcmZvcmVjYXN0YXJiaXRlci5vcmciLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvY2MxMTNkZjY5NmY4ZTlmMjA2Nzc5OTQzMzUxNzRhYjY_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ0ZS5wbmciLCJ1cGRhdGVkX2F0IjoiMjAxOS0wNC0wOFQyMDo1NjoyMS4zNjdaIiwiZW1haWwiOiJ0ZXN0aW5nQHNvbGFyZm9yZWNhc3RhcmJpdGVyLm9yZyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWJlMzQzZGY3MDI1NDA2MjM3ODIwYjg1IiwiYXVkIjoiUHJFMzlBZHRHTVBJNGdLMmhSdldaMmFEUmFyZnBnN0EiLCJpYXQiOjE1NTQ3NTcwNDYsImV4cCI6MTU1NDc5MzA0Nn0.FwhiPeNI7F_iyYZVUtu6KwsWx7Jl0Myqc5mUcSOv4n8neJcVz6I7LsdrFNYjBHCIVHVtYAfP6sey1imIVxeQ4sBvFJSyRd5jzbVbpPSLeB5cwLlgMRbTdRKQgDsuACdMus0tX3vJ3avdVHF0ystrwf9AQHCzzlYqvTjrgM0uZnXFP-jMhi4qyy-EUuTz0xq45DjybbDxpHqQcaQDWzL7IrH2KVv6JD4UbqkUyQLN8ThXwjoOanEHTnK1Df7Sh8K4PMuwk7_9xewv3HrpKjlQKecj3MiHUEOiaK0DVSFmXt7rCjF8dmACavNS-YIMviHUmjkJb1aZwfh_8aNPxvY2ew', # NOQA
        'scope': ['openid', 'profile', 'email'],
        'token_type': 'Bearer'
    },
    'userinfo': {
        'email': 'testing@solarforecastarbiter.org',
        'email_verified': False,
        'name': 'testing@solarforecastarbiter.org',
        'nickname': 'testing',
        'picture': 'https://s.gravatar.com/avatar/cc113df696f8e9f20677994335174ab6?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fte.png',
        'sub': 'auth0|5be343df7025406237820b85',
        'updated_at': '2019-04-08T20:56:21.367Z'}
}

@pytest.fixture()
def mocked_get(mocker):
    get = mocker.patch('sfa_dash.api_interface.observations.get_request')
    get.side_effect = InvalidClientIdError()
    return get


@pytest.fixture()
def authorized(app, auth_token):
    with app.test_request_context('/observations/'):
        app.blueprints['auth0'].authorized = True
        yield app

def test_token_refresh_error(app, mocked_get):
    with app.test_client() as webapp:
        req = webapp.get('/observations/')
    assert req.status_code == 302
    
def test_token_refresh_error_handler_called(authorized, mocked_get, mocker):
    handler = mocker.patch('sfa_dash.error_handlers.no_refresh_token')
    with authorized.test_client() as webapp:
        with webapp.session_transaction() as sess:
            sess['auth0_oauth_token'] = exp_oauth_token['auth0_oauth_token']
            sess['userinfo'] = exp_oauth_token['userinfo']
        pdb.set_trace()
        req = webapp.get('/observations/')
        assert 'test' == 'test'
    handler.assert_called()

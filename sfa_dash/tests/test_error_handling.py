import pdb
import pytest
import flask
from flask import current_app, request
from flask_dance.consumer.storage import MemoryStorage


from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError


import sfa_dash


exp_oauth_token = {'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJpc3MiOiJodHRwczovL3NvbGFyZm9yZWNhc3RhcmJpdGVyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1YmUzNDNkZjcwMjU0MDYyMzc4MjBiODUiLCJhdWQiOlsiaHR0cHM6Ly9hcGkuc29sYXJmb3JlY2FzdGFyYml0ZXIub3JnIiwiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTU0NzYzMjQ4LCJleHAiOjE1NTQ3NzQwNDgsImF6cCI6IlByRTM5QWR0R01QSTRnSzJoUnZXWjJhRFJhcmZwZzdBIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCJ9.UUhDH21mXEjuqrPrQBuLZjG2rjvg7vsfOGzyByXtYQxTeLpk8A4cnWUzjLPQv3DFR2qMMZk_ITMLpX-nBQDgnzVupnEmxNA3vSbBThbWrhIIMRxXf_X2M2HKXZ_zpdszLxnenQ_cAC_I6LM3p-6UHshWHi0RgnAg_x3T6p1GGk5lkT5-JjX39EEJBxkAT_QU7qkGbJm7gXAkjmAOFvMslJDdRz2HscRkYHvs1hlAlhTXEzNHzzIdxhy34qFpNzn4t6kdqt-6cToJKv2bI4PXOw6Y6qlaktUJeceuwXIU7sazYuvwO5RpnXdrb3sZvPLL2t3V46JnqiDbuVylZLSnWA', 'expires_at': 1554774048.760073, 'expires_in': 8564.166737, 'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJuaWNrbmFtZSI6InRlc3RpbmciLCJuYW1lIjoidGVzdGluZ0Bzb2xhcmZvcmVjYXN0YXJiaXRlci5vcmciLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvY2MxMTNkZjY5NmY4ZTlmMjA2Nzc5OTQzMzUxNzRhYjY_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ0ZS5wbmciLCJ1cGRhdGVkX2F0IjoiMjAxOS0wNC0wOFQyMjo0MDo0NC40NjZaIiwiZW1haWwiOiJ0ZXN0aW5nQHNvbGFyZm9yZWNhc3RhcmJpdGVyLm9yZyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWJlMzQzZGY3MDI1NDA2MjM3ODIwYjg1IiwiYXVkIjoiUHJFMzlBZHRHTVBJNGdLMmhSdldaMmFEUmFyZnBnN0EiLCJpYXQiOjE1NTQ3NjMyNDgsImV4cCI6MTU1NDc5OTI0OH0.FlChNngDhz6PtJxazHykwjiN48zWqVo9Fow2rITt_7kRyJUkMz8gfhWmJ_pKIAkOqVlkoi1bHDhvutPEPj9_JrwBnA2BXzBG4qFnohW6bFPAt5Ewc6GmZEVmR8Svra8XdDux2jVOvlJ5_Ndv6iHUF3YRuo9avHlVRW5dLlEtc5x_E8kSrR7lGbo6Jx5Ng9lNte50aXVv8LoBWQ5Du8Nl5oeBIFfsyb5kyhXdTjn5DCJZSoP_FdOUF51YviDFRC_d7Cg_qoSsC1djUbYMHFjEH_UNAprIie2HFKJX8CMDc1NHcq6sQtiF_tUfvfmg2-ghw9k98Ixe8e71Vr3eqQ03yg', 'scope': ['openid', 'profile', 'email'], 'token_type': 'Bearer'} 


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
    
def test_token_refresh_error_handler_called(app, mocker):
    handler = mocker.patch('sfa_dash.error_handlers.no_refresh_token')
    with app.test_client() as webapp:
        with webapp.session_transaction() as sess:
            sess['auth0_oauth_token'] = exp_oauth_token
        req = webapp.get('/observations/', base_url='https://localhost')
    handler.assert_called()

import pdb
import os
import requests


import pytest


from sfa_dash import create_app

BASE_URL='http://localhost'


no_arg_routes = [ 
    '/observations/', '/forecasts/']


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
        token = token_req.json()
        return token

@pytest.fixture()
def expired_token():
    stored = {'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJpc3MiOiJodHRwczovL3NvbGFyZm9yZWNhc3RhcmJpdGVyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1YmUzNDNkZjcwMjU0MDYyMzc4MjBiODUiLCJhdWQiOlsiaHR0cHM6Ly9hcGkuc29sYXJmb3JlY2FzdGFyYml0ZXIub3JnIiwiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTU1NDU0NzcwLCJleHAiOjE1NTU0NjU1NzAsImF6cCI6IlByRTM5QWR0R01QSTRnSzJoUnZXWjJhRFJhcmZwZzdBIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyJ9.lT1XPtLkYCVGUZjcAgWFCU6AJbKWtE077zw_KO4fhIaF0wo6TTpLTkZBmF9Sxmrwb5NfeR5XuJmkX3SPCjpzcZG9wdXIpPWRGhsOAAUdoSkoHKFzALoc46VPjA3A5SZxlGqNeh6RoKFlWRAp5EJN9Z-JcwT06JyJGrbx7ip4tCbAADqWuDY2tzkjKD3EHjHTO9OSJiCRxlNA22OCfMTF6B8-8RLUabZ414bypezw83S9g25mLLWtlGhQvzWGA8F7yhhVXbEsAPPC1QoyjevXzn8PBqL5dSDp6u1gL6T29PsbhZ0diZ1xt5jkm4iX-cryc7tqwq-5D5ZkC3wbhNpLuQ', 'refresh_token': 'QlLHR9wyFS5cokItX-ym7jWlCCuLO1fC3AtZLUeDVX-mI', 'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5UZENSRGRFTlVNMk9FTTJNVGhCTWtRelFUSXpNRFF6TUVRd1JUZ3dNekV3T1VWR1FrRXpSUSJ9.eyJuaWNrbmFtZSI6InRlc3RpbmciLCJuYW1lIjoidGVzdGluZ0Bzb2xhcmZvcmVjYXN0YXJiaXRlci5vcmciLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvY2MxMTNkZjY5NmY4ZTlmMjA2Nzc5OTQzMzUxNzRhYjY_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ0ZS5wbmciLCJ1cGRhdGVkX2F0IjoiMjAxOS0wNC0xNlQyMjo0NjoxMC42NTdaIiwiZW1haWwiOiJ0ZXN0aW5nQHNvbGFyZm9yZWNhc3RhcmJpdGVyLm9yZyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9zb2xhcmZvcmVjYXN0YXJiaXRlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWJlMzQzZGY3MDI1NDA2MjM3ODIwYjg1IiwiYXVkIjoiUHJFMzlBZHRHTVBJNGdLMmhSdldaMmFEUmFyZnBnN0EiLCJpYXQiOjE1NTU0NTQ3NzAsImV4cCI6MTU1NTQ5MDc3MH0.axw45-ms_LVIS_WsUdcCryZeOwpZVAn95zbUm9WO23bpIja7QaR1h6_Emb9nUNJIk44vp-J-zwKIZd4j7bg5_vaVcJER4_rL8vlc6f5lJdZAU20yeisTT4q1YcwlvQhg7avWMUkZaiO3SgK0eJ3371Gm2gJgK2b21bnpzmUHQ0vS906GLGngaVzb3VEE_g4CgR4u6qmBQRwq3Z6DyRBq572Qhn3TXk_0Xvj43Q9TyYjV5ioou5Xe-3T5HHsCoUWqDp0BZ3bP9FlYFws9DffnFzf1yVtpwfk9shmAe8V6Fn9N0OjuS4LJP0Tc-I7adspJlYfB9BeTEci6MKn58OQCrw', 'scope': ['openid', 'profile', 'email', 'offline_access'], 'expires_in': 0, 'token_type': 'Bearer', 'expires_at': 1555465570.9597309}  # NOQA
    return stored


@pytest.fixture()
def mocked_storage(mocker, auth_token, expired_token):
    def make_storage(authenticated=False):
        if authenticated:
            token = auth_token
        else:
            token = expired_token
        class fake_storage:
            def __init__(*args, **kwargs):
                pass

            def get(self, *args):
                return token

            def set(self, *args):
                pass

            def delete(self, *args):
                pass
        return fake_storage
    return make_storage


@pytest.fixture()
def mocked_unauth_storage(mocker, mocked_storage):
    storage = mocker.patch('sfa_dash.session_storage',
                           new=mocked_storage())


@pytest.fixture()
def mocked_auth_storage(mocker, mocked_storage):
    storage = mocker.patch('sfa_dash.session_storage',
                           new=mocked_storage(True))


@pytest.fixture()
def app_unauth(mocked_unauth_storage):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    return create_app('sfa_dash.config.TestConfig')


@pytest.fixture()
def app(mocked_auth_storage):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    return create_app('sfa_dash.config.TestConfig')


admin_routes_list = [
    '/admin/permissions/<uuid>',
    '/admin/users/<uuid>',
    '/admin/roles/<uuid>',
    '/admin/permissions/create/cdf_forecast_group',
    '/admin/permissions/create/observation',
    '/admin/permissions/create/forecast',
    '/admin/permissions/create/report',
    '/admin/permissions/create/site',
    '/admin/roles/create',
    '/admin/permissions/',
    '/admin/roles/',
    '/admin/users/',
    '/admin/permissions/<uuid>/delete',
    '/admin/roles/<uuid>/delete',
    '/admin/permissions/<uuid>/add',
    '/admin/users/<uuid>/add/',
    '/admin/roles/<uuid>/add/',
    '/admin/permissions/<uuid>/remove/<object_id>',
    '/admin/roles/<uuid>/remove/<permission_id>',
    '/admin/users/<uuid>/remove/<role_id>',
    '/admin/roles/<uuid>/grant/']


no_arg_routes_list = [
    '/sites/',
    '/observations/',
    '/forecasts/single/',
    '/forecasts/cdf/',
    '/reports/']


create_form_routes_list = [
    '/sites/create',
    '/sites/<uuid>/forecasts/single/create',
    '/sites/<uuid>/forecasts/cdf/create',
    '/sites/<uuid>/observations/create',
    '/sites/<uuid>/observations/create',
    '/reports/create',
    '/observations/<uuid>/download',
    '/forecasts/single/<uuid>/download',
    '/forecasts/cdf/<uuid>/download']


delete_form_routes_list = [
    '/observations/<uuid>/delete',
    '/forecasts/single/<uuid>/delete',
    '/forecasts/cdf/<uuid>/delete',
    '/reports/<uuid>/delete',
    '/sites/<uuid>/delete']


upload_form_routes_list = [
    '/observations/<uuid>/upload',
    '/forecasts/cdf/single/<uuid>/upload',
    '/forecasts/single/<uuid>/upload',]


single_object_routes_list = [
    '/sites/<uuid>/',
    '/observations/<uuid>',
    '/forecasts/cdf/single/<uuid>',
    '/forecasts/single/<uuid>',
    '/forecasts/cdf/<uuid>',
    '/reports/<uuid>']

# 
test_metadata_dict = {
    'observation': {},
    'forecast': {},
    'cdf_forecast': {},
    'report': {},
    'user': {},
    'permission': {},
    'role': {},
}
@pytest.fixture(params=no_arg_routes_list)
def no_arg_route(request):
    return request.param

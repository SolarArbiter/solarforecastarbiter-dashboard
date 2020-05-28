import os
import requests


import pymysql
import pytest
from flask import url_for


from sfa_dash import create_app

BASE_URL = 'http://localhost'


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
    mocker.patch('sfa_dash.session_storage',
                 new=mocked_storage())


@pytest.fixture()
def mocked_auth_storage(mocker, mocked_storage):
    mocker.patch('sfa_dash.session_storage',
                 new=mocked_storage(True))


@pytest.fixture()
def app_unauth(mocked_unauth_storage):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    return create_app('sfa_dash.config.TestConfig')


@pytest.fixture()
def app(mocked_auth_storage):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    return create_app('sfa_dash.config.TestConfig')


@pytest.fixture()
def client(app):
    yield app.test_client()


no_arg_routes_list = [
    '/sites/',
    '/observations/',
    '/forecasts/single/',
    '/forecasts/cdf/',
    '/reports/',
    '/aggregates/',
    '/sites/create',
    '/reports/create',
    '/aggregates/create',
]


@pytest.fixture(params=no_arg_routes_list)
def no_arg_route(request):
    return request.param


admin_routes_list = [
    '/admin/permissions/create/cdf_forecast_group',
    '/admin/permissions/create/observation',
    '/admin/permissions/create/forecast',
    '/admin/permissions/create/report',
    '/admin/permissions/create/site',
    '/admin/roles/create',
    '/admin/permissions/',
    '/admin/roles/',
    '/admin/users/',
]


@pytest.fixture(params=admin_routes_list)
def admin_route(request):
    return request.param


admin_multiarg_route_list = [
    '/admin/permissions/{permission_id}/remove/{object_id}',
    '/admin/roles/{role_id}/remove/{permission_id}',
    '/admin/users/{user_id}/remove/{role_id}',
]


@pytest.fixture(params=admin_multiarg_route_list)
def admin_multiarg_route(request):
    def fn(object_id, permission_id, user_id, role_id):
        return request.param.format(
            object_id=object_id,
            permission_id=permission_id,
            user_id=user_id,
            role_id=role_id)

    return fn


user_id_route_list = [
    '/admin/users/{user_id}',
    '/admin/users/{user_id}/add/',
]


@pytest.fixture(params=user_id_route_list)
def user_id_route(request):
    def fn(user_id):
        return request.param.format(user_id=user_id)
    return fn


role_id_route_list = [
    '/admin/roles/{role_id}',
    '/admin/roles/{role_id}/delete',
    '/admin/roles/{role_id}/add/',
    '/admin/roles/{role_id}/grant/',
]


@pytest.fixture(params=role_id_route_list)
def role_id_route(request):
    def fn(role_id):
        return request.param.format(role_id=role_id)
    return fn


permission_id_route_list = [
    '/admin/permissions/{permission_id}',
    '/admin/permissions/{permission_id}/delete',
    '/admin/permissions/{permission_id}/add',
]


@pytest.fixture(params=permission_id_route_list)
def permission_id_route(request):
    def fn(permission_report):
        return request.param.format(permission_id=permission_id)
    return fn


report_id_route_list = [
    '/reports/{report_id}',
    '/reports/{report_id}/delete',
]


@pytest.fixture(params=report_id_route_list)
def report_id_route(request):
    def fn(report_id):
        return request.param.format(report_id=report_id)
    return fn


site_id_route_list = [
    '/sites/{site_id}/',
    '/sites/{site_id}/delete',
    '/sites/{site_id}/forecasts/single/create',
    '/sites/{site_id}/forecasts/cdf/create',
    '/sites/{site_id}/observations/create',
    '/sites/{site_id}/observations/create',
]


@pytest.fixture(params=site_id_route_list)
def site_id_route(request):
    def fn(site_id):
        return request.param.format(site_id=site_id)
    return fn


observation_id_route_list = [
    '/observations/{observation_id}',
    '/observations/{observation_id}/upload',
    '/observations/{observation_id}/delete',
]


@pytest.fixture(params=observation_id_route_list)
def observation_id_route(request):
    def fn(observation_id):
        return request.param.format(observation_id=observation_id)
    return fn


forecast_id_route_list = [
    '/forecasts/single/{forecast_id}',
    '/forecasts/single/{forecast_id}/upload',
    '/forecasts/single/{forecast_id}/delete',
]


@pytest.fixture(params=forecast_id_route_list)
def forecast_id_route(request):
    def fn(forecast_id):
        return request.param.format(forecast_id=forecast_id)
    return fn


cdf_forecast_id_route_list = [
    '/forecasts/cdf/{forecast_id}',
    '/forecasts/cdf/{forecast_id}/delete',
]


@pytest.fixture(params=cdf_forecast_id_route_list)
def cdf_forecast_id_route(request):
    def fn(forecast_id):
        return request.param.format(forecast_id=forecast_id)
    return fn


cdf_forecast_single_id_routes_list = [
    '/forecasts/cdf/single/{forecast_id}/upload',
    '/forecasts/cdf/single/{forecast_id}',
]


@pytest.fixture(params=cdf_forecast_single_id_routes_list)
def cdf_forecast_single_id_route(request):
    def fn(forecast_id):
        return request.param.format(forecast_id=forecast_id)
    return fn


aggregate_id_route_list = [
    '/aggregates/{aggregate_id}',
    '/aggregates/{aggregate_id}/delete',
    '/aggregates/{aggregate_id}/add',
]


@pytest.fixture(params=aggregate_id_route_list)
def aggregate_id_route(request):
    def fn(aggregate_id):
        return request.param.format(aggregate_id=aggregate_id)
    return fn


test_metadata_dict = {
    'aggregate': {},
    'observation': {},
    'forecast': {},
    'cdf_forecast': {},
    'report': {},
    'user': {},
    'permission': {},
    'role': {},
}


@pytest.fixture()
def missing_id():
    return '7d2c3208-5243-11e9-8647-d663bd873d93'


@pytest.fixture()
def observation_id():
    return '123e4567-e89b-12d3-a456-426655440000'


@pytest.fixture()
def cdf_forecast_group_id():
    return 'ef51e87c-50b9-11e9-8647-d663bd873d93'


@pytest.fixture()
def cdf_forecast_id():
    return '633f9396-50bb-11e9-8647-d663bd873d93'


@pytest.fixture()
def forecast_id():
    return '11c20780-76ae-4b11-bef1-7a75bdc784e3'


@pytest.fixture()
def site_id():
    return 'd2018f1d-82b1-422a-8ec4-4e8b3fe92a4a'


@pytest.fixture()
def site_id_plant():
    return '123e4567-e89b-12d3-a456-426655440002'


@pytest.fixture()
def test_orgid():
    return 'b76ab62e-4fe1-11e9-9e44-64006a511e6f'


@pytest.fixture()
def user_id():
    return '0c90950a-7cca-11e9-a81f-54bf64606445'


@pytest.fixture()
def aggregate_id():
    return '458ffc27-df0b-11e9-b622-62adb5fd6af0'


@pytest.fixture()
def report_id():
    return '9f290dd4-42b8-11ea-abdf-f4939feddd82'


@pytest.fixture()
def test_url(app):
    def fn(view):
        with app.test_request_context():
            return url_for(view, _external=True)
    return fn


@pytest.fixture(scope='session')
def connection():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT', '3306')),
        user='root',
        password='testpassword',
        database='arbiter_data',
        binary_prefix=True)
    # with no connection.commit(), no data should stay in db
    return connection


@pytest.fixture()
def cursor(connection):
    connection.rollback()
    return connection.cursor()


@pytest.fixture()
def dictcursor(connection):
    connection.rollback()
    return connection.cursor(cursor=pymysql.cursors.DictCursor)


@pytest.fixture()
def role_id(cursor):
    cursor.execute(
        'SELECT BIN_TO_UUID(id, 1) from arbiter_data.roles '
        'WHERE name = "Test user role"')
    role_id = cursor.fetchone()[0]
    return role_id


@pytest.fixture()
def permission_id(cursor, role_id):
    cursor.execute(
        'SELECT BIN_TO_UUID(id, 1) FROM arbiter_data.permissions '
        'WHERE id IN (SELECT permission_id FROM '
        'arbiter_data.role_permission_mapping WHERE role_id '
        '= UUID_TO_BIN(%s, 1) ) LIMIT 1', role_id)
    permission_id = cursor.fetchone()[0]
    return permission_id



@pytest.fixture()
def permission_object_type(cursor, permission_id):
    cursor.execute(
        'SELECT object_type FROM arbiter_data.permissions '
        'WHERE id = UUID_TO_BIN(%s, 1)', permission_id)
    return cursor.fetchone()[0]


@pytest.fixture()
def valid_permission_object_id(
        observation_id, forecast_id, cdf_forecast_group_id, aggregate_id,
        site_id, role_id, user_id, permission_id, report_id,
        permission_object_type):
    ot = permission_object_type
    if ot == 'forecasts':
        return forecast_id
    if ot == 'observations':
        return observation_id
    if ot == 'cdf_forecasts':
        return cdf_forecast_group_id
    if ot == 'agggregates':
        return aggregate_id
    if ot == 'sites':
        return site_id
    if ot == 'reports':
        return report_id
    if ot == 'users':
        return user_id
    if ot == 'permissions':
        return permission_id
    if ot == 'roles':
        return role_id

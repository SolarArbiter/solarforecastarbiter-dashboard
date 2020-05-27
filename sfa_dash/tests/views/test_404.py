import pytest


from sfa_dash.conftest import BASE_URL


@pytest.fixture
def dne_uuid():
    return 'b6984bb8-9930-11ea-8541-54be64636445'


@pytest.mark.parametrize('route', [
    '/observations/',
    '/forecasts/single/',
    '/forecasts/cdf/',
])
def test_listing_filter_bad_site(client, route, dne_uuid):
    resp = client.get(route, base_url=BASE_URL,
                      query_string={'site_id': dne_uuid})
    assert "<b>404: </b>" in resp.data.decode('utf-8')


@pytest.mark.parametrize('route', [
    '/observations/',
    '/forecasts/single/',
    '/forecasts/cdf/',
])
def test_listing_filter_bad_aggregate(client, route, dne_uuid):
    resp = client.get(route, base_url=BASE_URL,
                      query_string={'aggregate_id': dne_uuid})
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_get_observation_routes(client, observation_id_route, dne_uuid):
    resp = client.get(observation_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_get_forecast_routes(client, forecast_id_route, dne_uuid):
    resp = client.get(forecast_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_get_site_routes(client, site_id_route, dne_uuid):
    resp = client.get(site_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_get_cdf_forecast_routes(
        client, cdf_forecast_id_route, dne_uuid):
    resp = client.get(cdf_forecast_id_route(dne_uuid),
                      base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_user_id_routes(client, user_id_route, dne_uuid):
    resp = client.get(user_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_permission_id_routes(client, permission_id_route, dne_uuid):
    resp = client.get(permission_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_role_id_routes(client, role_id_route, dne_uuid):
    resp = client.get(role_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')


def test_aggregate_id_routes(client, aggregate_id_route, dne_uuid):
    resp = client.get(aggregate_id_route(dne_uuid), base_url=BASE_URL)
    assert "<b>404: </b>" in resp.data.decode('utf-8')

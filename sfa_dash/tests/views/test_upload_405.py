import pytest


from sfa_dash.conftest import BASE_URL


@pytest.fixture
def upload_routes(forecast_id, observation_id, cdf_forecast_id):
    return [
        f'/forecasts/single/{forecast_id}/upload',
        f'/observations/{observation_id}/upload',
        f'/forecasts/cdf/single/{cdf_forecast_id}/upload']


@pytest.fixture(params=[0,1,2])
def single_upload_route(request, upload_routes):
    return upload_routes[request.param]


def assert_upload_get_not_allowed(client, single_upload_routes):
    resp = client.get(single_upload_routes,
                      base_url=BASE_URL)
    assert resp.status_code == 405

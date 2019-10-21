import json
import pytest
from requests import Response


from sfa_dash.blueprints.util import handle_response
from sfa_dash.errors import DataRequestException


@pytest.fixture()
def mock_response(mocker):
    def fn(status_code, json={}):
        resp = mocker.Mock()
        resp.status_code = status_code
        return resp
    return fn

@pytest.mark.parametrize('code', [
    400, 401, 404, 500, 502, 504])
def test_handle_response_requesterror(mock_response, code):
    with pytest.raises(DataRequestException):
        handle_response(mock_response(code))


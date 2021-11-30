from sfa_dash.api_interface import get_request


def list_outages():
    req = get_request(f'/outages')
    return req

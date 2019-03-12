from sfa_dash.api_interface import get_request, post_request

def get_metadata(obs_id):
    r = get_request(f'/observations/{obs_id}/metadata')
    return r.json()


def get_values(obs_id):
    r = get_request(f'/observations/{obs_id}/values')
    return r.json()


def list_metadata(site_id=None):
    if site_id is not None:
        r = get_request(f'/sites/{site_id}/observations')
    else:
        r = get_request('/observations/')
    return r.json()

def post_metadata(obs_dict):
    r = post_request('/observations/')
    return r.json()

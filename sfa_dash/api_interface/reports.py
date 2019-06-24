from sfa_dash.api_interface import get_request, post_request, delete_request


def get_metadata(report_id):
    req = get_request(f'/reports/{report_id}')
    return req


def list_metadata(site_id=None):
    if site_id is not None:
        req = get_request(f'/sites/{site_id}/reports')
    else:
        req = get_request('/reports/')
    return req


def post_metadata(report_dict):
    req = post_request('/reports/', report_dict)
    return req


def delete(report_id):
    req = delete_request(f'/reports/{report_id}')
    return req

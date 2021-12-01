from sfa_dash.api_interface import get_request, post_request, delete_request


def get_metadata(report_id):
    report = get_request(f'/reports/{report_id}')
    return report


def list_metadata():
    reports = get_request('/reports/')
    return reports


def post_metadata(report_dict):
    success = post_request('/reports/', report_dict)
    return success


def delete(report_id):
    delete = delete_request(f'/reports/{report_id}')
    return delete


def recompute(report_id):
    recompute = get_request(f'/reports/{report_id}/recompute')
    return recompute


def get_outages(report_id):
    outages = get_request(f'/reports/{report_id}/outages')
    return outages


def post_outage(report_id, outage_dict):
    outage_id = post_request(f'/reports/{report_id}/outages', outage_dict)
    return outage_id


def delete_outage(report_id, outage_id):
    delete = delete_request(f'/reports/{report_id}/outages/{outage_id}')
    return delete

"""Helper functions for all Solar Forecast Arbiter /sites/* endpoints.
"""
from sfa_dash.api_interface import get_request, post_request, delete_request


def list_metadata():
    r = get_request('/sites/')
    return r


def get_metadata(site_id):
    r = get_request(f'/sites/{site_id}')
    return r


def post_metadata(site_dict):
    r = post_request('/sites/', site_dict, json=True)
    return r


def delete(site_id):
    req = delete_request(f'/sites/{site_id}')
    return req


def update(site_id, updates):
    req = post_request(f'/sites/{site_id}', updates)
    return req

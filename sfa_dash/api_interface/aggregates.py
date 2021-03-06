"""Helper functions for all Solar Forecast Arbiter /aggregates/* endpoints.
"""
from sfa_dash.api_interface import get_request, post_request, delete_request


def list_metadata():
    req = get_request('/aggregates/')
    return req


def get_metadata(aggregate_id):
    req = get_request(f'/aggregates/{aggregate_id}/metadata')
    return req


def get_values(aggregate_id, **kwargs):
    req = get_request(f'/aggregates/{aggregate_id}/values', **kwargs)
    return req


def post_metadata(aggregate_dict):
    req = post_request('/aggregates/', aggregate_dict, json=True)
    return req


def update(aggregate_id, updates):
    req = post_request(f'/aggregates/{aggregate_id}/metadata',
                       updates, json=True)
    return req


def delete(aggregate_id):
    req = delete_request(f'/aggregates/{aggregate_id}')
    return req


def delete_observation(aggregate_id, observation_id):
    req = delete_request(
        f'/aggregates/{aggregate_id}/observations/{observation_id}')
    return req

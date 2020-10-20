from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor


from flask import copy_current_request_context
from flask.globals import _app_ctx_stack
import pandas as pd


from sfa_dash.api_interface import get_request, post_request, delete_request
from sfa_dash.api_interface.cdf_forecasts import get_values as get_cdf_values
from sfa_dash.api_interface.cdf_forecasts import valid_times as cdf_valid_times
from solarforecastarbiter.io.utils import json_payload_to_forecast_series


def get_metadata(forecast_id):
    req = get_request(f'/forecasts/cdf/{forecast_id}')
    return req


def with_app_context(func):
    app_context = _app_ctx_stack.top

    def wrapper(*args, **kwargs):
        with app_context:
            return func(*args, **kwargs)

    return wrapper


def get_values(metadata, **kwargs):
    """
    Parameters
    ----------
    metadata: dict
        The metadata dictionary of a probabilistic forecast group as returned
        from the API.

    Returns
    -------
    pandas.DataFrame
        Dataframe where column names are constant values.
    """
    constant_values = metadata['constant_values']

    @with_app_context
    @copy_current_request_context
    def request_constant_value_values(cv):
        """Function to pass to ThreadPoolExecutor to make a request against
        the API while maintaining the Request/App context and the current user
        session.
        """
        return (
            str(cv['constant_value']),
            json_payload_to_forecast_series(
                get_cdf_values(cv["forecast_id"], **kwargs)
            )
        )

    # collect a list of tuple, series objects asynchronously
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_series = executor.map(
            request_constant_value_values,
            constant_values
        )
    return pd.DataFrame.from_records(OrderedDict(all_series))


def list_metadata(site_id=None, aggregate_id=None):
    if site_id is not None:
        req = get_request(f'/sites/{site_id}/forecasts/cdf')
    elif aggregate_id is not None:
        req = get_request(f'/aggregates/{aggregate_id}/forecasts/cdf')
    else:
        req = get_request('/forecasts/cdf/')
    return req


def post_metadata(forecast_dict):
    req = post_request('/forecasts/cdf/', forecast_dict)
    return req


def delete(forecast_id):
    req = delete_request(f'/forecasts/cdf/{forecast_id}')
    return req


def valid_times(metadata):
    constant_values = metadata['constant_values']
    cv_timeranges = [cdf_valid_times(cv['forecast_id'])
                     for cv in constant_values]
    mins = pd.to_datetime([c['min_timestamp'] for c in cv_timeranges])
    maxs = pd.to_datetime([c['max_timestamp'] for c in cv_timeranges])
    time_min = mins.min()
    time_max = maxs.max()
    if pd.isna(time_min):
        start = None
    else:
        start = time_min.isoformat()
    if pd.isna(time_max):
        end = None
    else:
        end = time_max.isoformat()
    return {
        'forecast_id': metadata['forecast_id'],
        'min_timestamp': start,
        'max_timestamp': end,
    }


def update(forecast_id, updates):
    req = post_request(f'/forecasts/cdf/{forecast_id}', updates)
    return req

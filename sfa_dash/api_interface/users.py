from requests.exceptions import HTTPError


from sfa_dash.api_interface import get_request, post_request, delete_request
from sfa_dash.errors import DataRequestException


def get_metadata(user_id):
    try:
        req = get_request(f'/users/{user_id}')
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to load user info, please wait a minute "
                           "and try again."]
            })
    return req


def list_metadata():
    try:
        req = get_request('/users/')
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to load user list, please wait a minute "
                           "and try again."]
            })
    return req


def current():
    req = get_request('/users/current')
    return req


def add_role(user_id, role_id):
    req = post_request(f'/users/{user_id}/roles/{role_id}', payload=None)
    return req


def remove_role(user_id, role_id):
    req = delete_request(f'/users/{user_id}/roles/{role_id}')
    return req


def get_metadata_by_email(email):
    try:
        req = get_request(f'/users-by-email/{email}')
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to retrieve user by email, please wait a "
                           "minute and try again."]
            })
    return req


def add_role_by_email(email, role_id):
    try:
        req = post_request(f'/users-by-email/{email}/roles/{role_id}',
                           payload=None)
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to grant role by email, please wait a "
                           "minute and try again."]
            })
    return req


def remove_role_by_email(email, role_id):
    try:
        req = delete_request(f'/users-by-email/{email}/roles/{role_id}')
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to remove role by email, please wait a "
                           "minute and try again."]
            })
    return req


def get_email(user_id):
    try:
        req = get_request(f'/users/{user_id}/email')
    except HTTPError as e:
        if e.response.status_code == 500:
            raise DataRequestException(500, {
                "errors": ["Failed to look up user email, please wait a "
                           "minute and try again."]
            })
    return req


def actions_on(uuid):
    req = get_request(f'/users/actions-on/{uuid}')
    return req


def actions_on_type(object_type):
    """Get a list of objects and actions user can perform on them.

    Parameters
    ----------
    object_type: str
        The type of object to query for. Note that the api uses plural type
        notation, e.g. `observations`.
    Returns
    -------
    dict
        Dictionary where keys are object uuids and values are a list of
        permitted actions.
    """
    req = get_request(f'/users/actions-on-type/{object_type}')
    actions_dict = {obj['object_id']: obj['actions'] for obj in req['objects']}
    return actions_dict


def get_create_permissions():
    req = get_request('/users/can-create/')
    return req

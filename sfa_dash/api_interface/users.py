from sfa_dash.api_interface import get_request, post_request, delete_request


def get_metadata(user_id):
    req = get_request(f'/users/{user_id}')
    return req


def list_metadata():
    req = get_request('/users/')
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
    req = get_request(f'/users-by-email/{email}')
    return req


def add_role_by_email(email, role_id):
    req = post_request(f'/users-by-email/{email}/roles/{role_id}',
                       payload=None)
    return req


def remove_role_by_email(email, role_id):
    req = delete_request(f'/users-by-email/{email}/roles/{role_id}')
    return req


def get_email(user_id):
    req = get_request(f'/users/{user_id}/email')
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

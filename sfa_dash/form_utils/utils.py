def parse_timedelta(data_dict, key_root):
    """Parse values from a timedelta form element, and return the value in
    minutes

    Parameters
    ----------
    data_dict: dict
        Dictionary of posted form data

    key_root: string
        The shared part of the name attribute of the inputs to parse.
        e.g. 'lead_time' will parse and concatenate 'lead_time_number'
        and 'lead_time_units'

    Returns
    -------
    int
        The number of minutes in the Timedelta.
    """
    value = int(data_dict[f'{key_root}_number'])
    units = data_dict[f'{key_root}_units']
    if units == 'minutes':
        return value
    elif units == 'hours':
        return value * 60
    elif units == 'days':
        return value * 1440


def parse_hhmm_field(data_dict, key_root):
    """ Extracts and parses the hours and minutes inputs to create a
    parseable time of day string in HH:MM format. These times are
    displayed as two select fields designated with a name (key_root)
    and _hours or _minutes suffix.

    Parameters
    ----------
    data_dict: dict
        Dictionary of posted form data

    key_root: string
        The shared part of the name attribute of the inputs to parse.
        e.g. 'issue_time' will parse and concatenate 'issue_time_hours'
        and 'issue_time_minutes'

    Returns
    -------
    string
        The time value in HH:MM format.
    """
    hours = int(data_dict[f'{key_root}_hours'])
    minutes = int(data_dict[f'{key_root}_minutes'])
    return f'{hours:02d}:{minutes:02d}'


def flatten_dict(to_flatten):
    """Flattens nested dictionaries, removing keys of the nested elements.
    Useful for flattening API responses for prefilling forms on the
    dashboard.
    """
    flattened = {}
    for key, value in to_flatten.items():
        if isinstance(value, dict):
            flattened.update(flatten_dict(value))
        else:
            flattened[key] = value
    return flattened


def set_location_id(form_data, forecast_metadata):
    if 'site_id' in form_data:
        forecast_metadata['site_id'] = form_data.get('site_id')
    if 'aggregate_id' in form_data:
        forecast_metadata['aggregate_id'] = form_data.get('aggregate_id')

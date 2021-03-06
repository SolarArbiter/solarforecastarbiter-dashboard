import pandas as pd


from solarforecastarbiter.datamodel import ALLOWED_VARIABLES, COMMON_NAMES


variable_mapping = COMMON_NAMES

data_type_mapping = {
    'site': 'Site',
    'observation': 'Observation',
    'forecast': 'Forecast',
    'cdf_forecast': 'Probabilistic Forecast',
    'cdf_forecast_group': 'Probabilistic Forecast Group',
    'report': 'Report',
    'aggregate': 'Aggregate',
}

# variables that require a site has modeling parameters
MODELING_PARAM_VARIABLES = ['ac_power', 'dc_power', 'poa_global',
                            'curtailment', 'availability']


def api_to_dash_varname(api_varname):
    return COMMON_NAMES[api_varname]


def api_varname_to_units(api_varname):
    return ALLOWED_VARIABLES[api_varname]


def human_friendly_datatype(data_type):
    return data_type_mapping[data_type]


def format_datetime(dt_string):
    """Temporary solution to formatting datetime strings returned by API
    """
    return pd.Timestamp(dt_string).strftime('%Y-%m-%d %H:%M:%SZ')


def display_timedelta(minutes):
    """Converts timedelta in minutes to human friendly format.

    Parameters
    ----------
    minutes: int

    Returns
    -------
    string
        The timedelta in 'x days y hours z minutes' format.

    Raises
    ------
    ValueError
        If the timedelta is negative.
    """
    def plural(num):
        if num != 1:
            return 's'
        else:
            return ''
    if minutes < 0:
        raise ValueError
    days = minutes // 1440
    hours = minutes // 60 % 24
    minutes = minutes % 60
    time_elements = []
    if days > 0:
        time_elements.append(f'{days} day{plural(days)}')
    if hours > 0:
        time_elements.append(f'{hours} hour{plural(hours)}')
    if minutes > 0 or (days == 0 and hours == 0):
        time_elements.append(f'{minutes} minute{plural(minutes)}')
    time_string = ' '.join(time_elements)
    return time_string


def is_number(num):
    return str(num).isnumeric()


def climate_zone_links(zones):
    def reference_zone_link(zone_name):
        if 'Reference Region' in zone_name:
            zone_number = zone_name.split(' ')[-1]
            return f'<a href="https://solarforecastarbiter.org/climatezones/#region{zone_number}">{zone_name}</a>'  # noqa: E501
        else:
            return zone_name
    if zones:
        return [reference_zone_link(zone) for zone in zones]
    else:
        return ["No Climate Zone"]


def site_variable_options(site_metadata):
    has_modeling_parameters = any(
        site_metadata['modeling_parameters'].values())
    variable_options = {key: f'{value} ({api_varname_to_units(key)})'
                        for key, value in variable_mapping.items()}
    if has_modeling_parameters:
        return variable_options
    else:
        return {k: v for k, v in variable_options.items()
                if k not in MODELING_PARAM_VARIABLES}


def register_jinja_filters(app):
    app.jinja_env.filters['convert_varname'] = api_to_dash_varname
    app.jinja_env.filters['var_to_units'] = api_varname_to_units
    app.jinja_env.filters['display_timedelta'] = display_timedelta
    app.jinja_env.filters['convert_data_type'] = human_friendly_datatype
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['is_number'] = is_number
    app.jinja_env.filters['climate_zone_links'] = climate_zone_links
    app.jinja_env.filters['site_variable_options'] = site_variable_options

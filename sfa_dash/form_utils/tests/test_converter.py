from copy import deepcopy


from sfa_dash.form_utils import converters


def without_extra(the_dict):
    new_dict = deepcopy(the_dict)
    new_dict.pop('extra_parameters', None)
    new_dict.pop('_links', None)
    new_dict.pop('forecast_id', None)
    new_dict.pop('observation_id', None)
    new_dict.pop('provider', None)
    new_dict.pop('created_at', None)
    new_dict.pop('modified_at', None)
    return new_dict


def test_site_converter_roundtrip_no_modeling(site):
    expected = without_extra(site)
    expected.pop('site_id')
    expected.pop('modeling_parameters')
    form_data = converters.SiteConverter.payload_to_formdata(site)
    api_data = converters.SiteConverter.formdata_to_payload(form_data)
    assert api_data == expected


def test_site_converter_roundtrip(site_with_modeling_params):
    expected = without_extra(site_with_modeling_params)
    expected.pop('site_id')

    none_keys = [k for k, v in expected['modeling_parameters'].items()
                 if v is None]
    for key in none_keys:
        expected['modeling_parameters'].pop(key)
    form_data = converters.SiteConverter.payload_to_formdata(
        site_with_modeling_params)
    api_data = converters.SiteConverter.formdata_to_payload(form_data)
    assert api_data == expected


def test_site_converter_payload_to_formdata(site):
    form_data = converters.SiteConverter.payload_to_formdata(site)
    assert form_data['name'] == 'Weather Station'
    assert form_data['elevation'] == 595.0
    assert form_data['latitude'] == 42.19
    assert form_data['longitude'] == -122.7
    assert form_data['timezone'] == 'Etc/GMT+8'
    assert form_data['site_type'] == 'weather-station'


def test_site_converter_payload_to_formdata_plant(site_with_modeling_params):
    form_data = converters.SiteConverter.payload_to_formdata(
        site_with_modeling_params)
    assert form_data['name'] == 'Power Plant 1'
    assert form_data['elevation'] == 786.0
    assert form_data['latitude'] == 43.73403
    assert form_data['longitude'] == -96.62328
    assert form_data['timezone'] == 'Etc/GMT+6'
    assert form_data['site_type'] == 'power-plant'
    assert form_data['ac_capacity'] == 0.015
    assert form_data['ac_loss_factor'] == 0.0
    assert form_data['dc_capacity'] == 0.015
    assert form_data['dc_loss_factor'] == 0.0
    assert form_data['surface_azimuth'] == 180.0
    assert form_data['surface_tilt'] == 45.0
    assert form_data['temperature_coefficient'] == -0.2
    assert form_data['tracking_type'] == 'fixed'


def test_site_converter_formdata_to_payload(site_with_modeling_params):
    form_data = {
        'name': 'Power Plant 1',
        'elevation': 786.0,
        'latitude': 43.73403,
        'longitude': -96.62328,
        'timezone': 'Etc/GMT+6',
        'site_type': 'power-plant',
        'ac_capacity': 0.015,
        'ac_loss_factor': 0.0,
        'dc_capacity': 0.015,
        'dc_loss_factor': 0.0,
        'surface_azimuth': 180.0,
        'surface_tilt': 45.0,
        'temperature_coefficient': -0.2,
        'tracking_type': 'fixed',
    }
    api_payload = converters.SiteConverter.formdata_to_payload(form_data)
    assert api_payload == {
        'name': 'Power Plant 1',
        'elevation': 786.0,
        'latitude': 43.73403,
        'longitude': -96.62328,
        'timezone': 'Etc/GMT+6',
        'modeling_parameters': {
            'ac_capacity': 0.015,
            'ac_loss_factor': 0.0,
            'dc_capacity': 0.015,
            'dc_loss_factor': 0.0,
            'surface_azimuth': 180.0,
            'surface_tilt': 45.0,
            'temperature_coefficient': -0.2,
            'tracking_type': 'fixed',
        },
    }


def test_site_observation_converter_roundtrip(observation):
    form_data = converters.ObservationConverter.payload_to_formdata(
        observation)
    api_data = converters.ObservationConverter.formdata_to_payload(form_data)
    assert api_data == without_extra(observation)


def test_observation_converter_payload_to_formdata():
    pass


def test_observation_converter_formdata_to_payload():
    pass


def test_site_forecast_converter_roundtrip(forecast):
    form_data = converters.ForecastConverter.payload_to_formdata(forecast)
    api_data = converters.ForecastConverter.formdata_to_payload(form_data)
    assert api_data == without_extra(forecast)


def test_forecast_converter_payload_to_formdata():
    pass


def test_forecast_converter_formdata_to_payload():
    pass

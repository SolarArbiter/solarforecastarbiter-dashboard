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


def test_site_converter_payload_to_formdata():
    pass


def test_site_converter_formdata_to_payload():
    pass


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

"""Contains converter objects for changing form submissions to api schema
compliant dictionaries for posting and vice versa.

Each converter subclasses the FormCoverter base class to enforce a common
interface. The converter's `form` attribute is the path of the form template
the converter is expected to parse.
"""
from abc import ABC, abstractmethod
from functools import reduce


from sfa_dash.form_utils import utils


class FormConverter(ABC):
    """Abstract base class to serve as an interface.
    """
    form = None

    @classmethod
    @abstractmethod
    def payload_to_formdata(cls, payload_dict):
        """Converts an API schema compliant dictionary to a dict used for
        prefilling form fields.

        Parameters
        ----------
        payload_dict: dict
            API json schema object parsed into a dictionary.

        Returns
        -------
        dict
            Dictionary that mirrors the format of Flask's request.form. Keys
            should be the name of the HTML input element.
        """
        pass

    @classmethod
    @abstractmethod
    def formdata_to_payload(cls, form_dict):
        """Converts a dictionary of form submission data into a API schema
        compliant dictionary to a dict used for

        Parameters
        ----------
        form_dict: dict
            Dictionary of form submission data. Usually just Flask's
            request.form dict.

        Returns
        -------
        payload_dict: dict
            API json schema object parsed into a dictionary.
        """
        pass


class SiteConverter(FormConverter):
    form = 'forms/site_form/html'
    tracking_keys = {
        'fixed': ['surface_tilt', 'surface_azimuth'],
        'single_axis': ['axis_azimuth', 'backtrack', 'axis_tilt',
                        'ground_coverage_ratio', 'max_rotation_angle'],
    }
    modeling_keys = ['ac_capacity', 'dc_capacity', 'ac_loss_factor',
                     'dc_loss_factor', 'temperature_coefficient',
                     'tracking_type']

    top_level_keys = ['name', 'elevation', 'latitude', 'longitude', 'timezone',
                      'extra_parameters']

    @classmethod
    def payload_to_formdata(cls, payload_dict):
        """Converts an api response to a form data dictionary for filling a
        form.

        Parameters
        ----------
        payload_dict: dict
            API json response as a python dict

        Returns
        -------
        dict
            dictionary of form data.
        """
        form_dict = {key: payload_dict[key]
                     for key in cls.top_level_keys
                     if key != 'extra_parameters'}
        is_plant = reduce(lambda a, b: a is not None or b is not None,
                          payload_dict['modeling_parameters'].values())
        if is_plant:
            form_dict['site_type'] = 'power-plant'
            modeling_params = payload_dict['modeling_parameters']
            for key in cls.modeling_keys:
                form_dict[key] = modeling_params[key]
            for key in cls.tracking_keys[modeling_params['tracking_type']]:
                form_dict[key] = modeling_params[key]
        else:
            form_dict['site_type'] = 'weather-station'
        return form_dict

    @classmethod
    def formdata_to_payload(cls, form_dict):
        """Formats the result of a site webform into an API payload.

        Parameters
        ----------
        form_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        site_metadata = {key: form_dict[key]
                         for key in cls.top_level_keys
                         if form_dict.get(key, "") != ""}
        if form_dict['site_type'] == 'power-plant':
            modeling_params = {key: form_dict[key]
                               for key in cls.modeling_keys
                               if form_dict.get(key, "") != ""}
            tracking_type = form_dict['tracking_type']
            tracking_fields = {key: form_dict[key]
                               for key in cls.tracking_keys[tracking_type]}
            modeling_params.update(tracking_fields)
            site_metadata['modeling_parameters'] = modeling_params
        return site_metadata


class ObservationConverter(FormConverter):
    form = 'forms/observation_form.html'

    @classmethod
    def payload_to_formdata(cls, payload_dict):
        pass

    @classmethod
    def formdata_to_payload(cls, form_dict):
        """Formats the result of a observation webform into an API payload.

        Parameters
        ----------
        form_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        observation_metadata = {}
        direct_keys = ['name', 'variable', 'interval_value_type',
                       'uncertainty', 'extra_parameters', 'interval_label',
                       'site_id']
        observation_metadata = {key: form_dict[key]
                                for key in direct_keys
                                if form_dict.get(key, "") != ""}
        observation_metadata['interval_length'] = utils.parse_timedelta(
            form_dict,
            'interval_length')
        return observation_metadata


class ForecastConverter(FormConverter):
    form = 'forms/forecast_form.html'

    @classmethod
    def payload_to_formdata(cls, payload_dict):
        pass

    @classmethod
    def formdata_to_payload(cls, form_dict):
        """Formats the result of a forecast webform into an API payload.

        Parameters
        ----------
        form_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        forecast_metadata = {}
        direct_keys = ['name', 'variable', 'interval_value_type',
                       'extra_parameters', 'interval_length',
                       'interval_label']
        forecast_metadata = {key: form_dict[key]
                             for key in direct_keys
                             if form_dict.get(key, '') != ''}
        utils.set_location_id(form_dict, forecast_metadata)
        forecast_metadata['issue_time_of_day'] = utils.parse_hhmm_field(
            form_dict,
            'issue_time')
        forecast_metadata['lead_time_to_start'] = utils.parse_timedelta(
            form_dict,
            'lead_time')
        forecast_metadata['run_length'] = utils.parse_timedelta(
            form_dict,
            'run_length')
        forecast_metadata['interval_length'] = utils.parse_timedelta(
            form_dict,
            'interval_length')
        return forecast_metadata


class CDFForecastConverter(FormConverter):
    form = 'forms/cdf_forecast_group_form.html'

    @classmethod
    def payload_to_formdata(cls, payload_dict):
        pass

    @classmethod
    def formdata_to_payload(cls, form_dict):
        """Formats the result of a cdf forecast webform into an API payload.

        Parameters
        ----------
        form_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        forecast_metadata = ForecastConverter.formdata_to_payload(form_dict)
        constant_values = form_dict['constant_values'].split(',')
        forecast_metadata['constant_values'] = constant_values
        forecast_metadata['axis'] = form_dict['axis']
        return forecast_metadata


class AggregateConverter(FormConverter):
    form = 'forms/aggregate_form.html'

    @classmethod
    def payload_to_formdata(cls, payload_dict):
        pass

    @classmethod
    def formdata_to_payload(cls, form_dict):
        formatted = {}
        formatted['name'] = form_dict['name']
        formatted['description'] = form_dict['description']
        formatted['interval_length'] = utils.parse_timedelta(
            form_dict, 'interval_length')
        formatted['interval_label'] = form_dict['interval_label']
        formatted['aggregate_type'] = form_dict['aggregate_type']
        formatted['timezone'] = form_dict['timezone']
        formatted['variable'] = form_dict['variable']
        formatted['extra_parameters'] = form_dict['extra_parameters']
        return formatted

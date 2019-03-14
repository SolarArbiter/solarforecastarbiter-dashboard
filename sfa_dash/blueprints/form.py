import pdb
from flask import Blueprint, jsonify, render_template, request, abort, redirect, url_for
from flask.views import MethodView
from sfa_dash.api_interface import sites, observations, forecasts
from sfa_dash.blueprints.base import BaseView
import json
import requests


class MetadataForm(BaseView):
    """Base form view.
    """
    def __init__(self, data_type):
        self.data_type = data_type
        if data_type == 'forecast':
            self.template = 'forms/forecast_form.html'
            self.id_key = 'forecast_id'
            self.api_handle = forecasts
            self.formatter = self.forecast_formatter
        if data_type == 'observation':
            self.template = 'forms/obs_form.html'
            self.id_key = 'obs_id'
            self.api_handle = observations
            self.formatter = self.observation_formatter
        if data_type == 'site':
            self.template = 'forms/site_form.html'
            self.id_key = 'site_id'
            self.api_handle = sites
            self.formatter = self.site_formatter
        
    def flatten_dict(self, to_flatten):
        """Flattens nested dictionaries, removing keys of the nested elements.
        Useful for flattening API responses for prefilling forms on the
        dashboard.
        """
        flattened = {}
        for key, value in to_flatten.items():
            if isinstance(value, dict):
                flattened.update(self.flatten_dict(value))
            else:
                flattened[key] = value
        return flattened


    def site_formatter(self, site_dict):
        """Formats the result of a site webform into an API payload.

        Parameters
        ----------
        site_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        modeling_keys = ['ac_capacity','dc_capacity',
                         'temperature_coefficient', 'axis_azimuth',
                         'tracking_type', 'backtrack',
                         'axis_tilt', 'ground_coverage_ratio',
                         'surface_tilt', 'surface_azimuth']
        top_level_keys = ['name', 'elevation', 'latitude',
                          'longitude', 'timezone', 'extra_parameters']
        site_metadata = { key: site_dict[key]
                          for key in top_level_keys
                          if site_dict.get(key, "") != ""} 
        modeling_params = { key: site_dict[key]
                            for key in modeling_keys
                            if site_dict.get(key, "") != ""}
        site_metadata['modeling_parameters'] = modeling_params
        return site_metadata


    def observation_formatter(self, observation_dict):
        """Formats the result of a observation webform into an API payload.

        Parameters
        ----------
        site_dict:  dict
            The posted form data parsed into a dict.
        Returns
        -------
        dictionary
            Form data formatted to the API spec.
        """
        observation_metadata = {}
        direct_keys = ['name', 'variable', 'value_type', 'uncertainty', 'extra_parameters',
                       'interval_label', 'site_id']
        observation_metadata = { key: observation_dict[key]
                                 for key in direct_keys
                                 if observation_dict.get(key, "") != ""} 
        #interval_length = f'{observaton_dict["interval_number"]} {observation_dict["interval_units"]}'
        #observation_dict['interval_length'] = interval_length
        return observation_metadata


    def forecast_formatter(self, forecast_dict):
        return forecast_dict
            
    def handle_api_error(self):
        pass

    def get(self):
        raise NotImplementedError

    def post(self):
        pass


class CreateForm(MetadataForm):
    def __init__(self, data_type):
        super().__init__(data_type)
    
    def get_site_metadata(self, site_id):
        site_metadata_request = sites.get_metadata(site_id)
        if site_metadata_request.status_code != 200:
            abort(404)
        site_metadata = site_metadata_request.json()
        return render_template('data/metadata/site_metadata.html',
                                   **site_metadata)

    def get(self):
        template_arguments = {}
        site_id = request.args.get('site_id')
        if site_id is not None:
            template_arguments['site_id'] = site_id
            template_arguments['metadata'] = self.get_site_metadata(site_id)
        return render_template(self.template, **template_arguments)

    def post(self):
        form_data = request.form
        formatted_form = self.formatter(form_data)
        response = self.api_handle.post_metadata(formatted_form)
        if response.status_code == 201:
            uuid = response.text
            return redirect(url_for(f'data_dashboard.{self.data_type}_view',
                                    uuid=uuid))
        elif response.status_code == 400:
            errors = response.json()['errors']
            errors = self.flatten_dict(errors)
            return render_template(self.template, form_data=form_data,
                                   errors=errors)
        elif response.status_code == 401:
            errors = { 'Unauthorized': f'You do not have permissions to create resources of type {self.data_type}'}
            return render_template(self.template, form_data=form_data, errors=errors)
        else:
            errors = { 'Error': 'Something went wrong, please contact a site administrator.'}
            return render_template(self.template, form_data=form_data, errors=errors)

class EditForm(MetadataForm):
    def __init__(self, data_type):
        super().__init__(data_type)


    def get(self, uuid):
        metadata = self.api_handle.get_metadata(uuid)
        return render_template(self.template, **metadata)



forms_blp = Blueprint('forms', 'forms')
forms_blp.add_url_rule('/sites/create', view_func=CreateForm.as_view('create_site', data_type='site'))
forms_blp.add_url_rule('/observations/create',
                       view_func=CreateForm.as_view('create_site_observation', data_type='observation'))
forms_blp.add_url_rule('/forecasts/create',
                       view_func=CreateForm.as_view('create_site_forecast', data_type='forecast'))

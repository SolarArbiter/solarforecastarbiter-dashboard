import pdb
from flask import Blueprint, jsonify, render_template, request, abort, redirect
from flask.views import MethodView
from sfa_dash.api_interface import sites, observations, forecasts
from sfa_dash.blueprints.base import BaseView
import json
import requests


class MetadataForm(BaseView):
    """
    """
    def __init__(self, data_type):
        self.data_type = data_type
        if data_type == 'forecast':
            self.template = 'forms/forecast_form.html'
            self.id_key = 'forecast_id'
            self.api_handle = forecasts
        if data_type == 'observation':
            self.template = 'forms/obs_form.html'
            self.id_key = 'obs_id'
            self.api_handle = observations
        if data_type == 'site':
            self.template = 'forms/site_form.html'
            self.id_key = 'site_id'
            self.api_handle = sites
        # TODO :remove this
        if data_type == 'test':
            self.template = 'forms/test_site_form.html'
            self.id_key = 'site_id'
            self.api_handle = sites

    def handle_api_error(self):
        pass

    def get(self):
        raise NotImplementedError

    def post(self):
        pass


class CreateForm(MetadataForm):
    def __init__(self, data_type):
        super().__init__(data_type)

    def get(self):
        template_arguments = {}
        site_id = request.args.get('site_id')
        if site_id is not None:
            site_metadata = sites.get_metadata(site_id)
            if not site_metadata:
                abort(404)
            template_arguments['metadata'] = render_template('data/metadata/site_metadata.html',
                                                             **site_metadata)
        return render_template(self.template, **template_arguments)

    def post(self):
        # TODO: some validation
        # TODO: add template args for types other than site.
        form_data = request.form
        response = self.api_handle.post_metadata(form_data)
        if response.status_code == 201:
            site_id = response.text
            return redirect(url_for('data_dashboard.site_view'), site_id=site_id)
        elif response.status_code == 400:
            errors = response.json()['errors']
            return render_template(self.template, metadata=form_data, errors=errors)
        elif response.status_code == 401:
            errors = { 'Unauthorized': f'You do not have permissions to create resources of type {self.data_type}'}
            return render_template(self.template, metadata=form_data, errors=errors)
        else:
            errors = { 'Error': 'Something went wrong, please contact a site administrator.'}
            return render_template(self.template, errors=errors)

class EditForm(MetadataForm):
    def __init__(self, data_type):
        super().__init__(data_type)


    def get(self, uuid):
        metadata = self.api_handle.get_metadata(uuid)
        return render_template(self.template, **metadata)

forms_blp = Blueprint('forms', 'forms')
#forms_blp.add_url_rule('/sites/create', view_func=CreateForm.as_view('create_site', data_type='site'))
forms_blp.add_url_rule('/sites/create', view_func=CreateForm.as_view('create_site', data_type='test'))

forms_blp.add_url_rule('/observations/create',
                       view_func=CreateForm.as_view('create_site_observation', data_type='observation'))
forms_blp.add_url_rule('/forecasts/create',
                       view_func=CreateForm.as_view('create_site_forecast', data_type='forecast'))

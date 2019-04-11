from flask import url_for, render_template, abort, redirect

from sfa_dash.api_interface import (sites, observations, forecasts,
                                    cdf_forecast_groups)
from sfa_dash.blueprints.dash import DataDashView


class DeleteConfirmation(DataDashView):
    def __init__(self, data_type):
        if data_type == 'forecast':
            self.api_handle = forecasts
            self.metadata_template = 'data/metadata/forecast_metadata.html'
        elif data_type == 'observation':
            self.api_handle = observations
            self.metadata_template = 'data/metadata/observation_metadata.html'
        elif data_type == 'cdf_forecast_group':
            self.api_handle = cdf_forecast_groups
            self.metadata_template = 'data/metadata/cdf_forecast_group_metadata.html' # NOQA
        elif data_type == 'site':
            self.api_handle = sites
            self.metadata_template = 'data/metadata/site_metadata.html'
        else:
            raise ValueError(f'No Deletetion Form defined for {data_type}.')
        self.data_type = data_type
        self.template = 'forms/deletion_form.html'

    def template_args(self, **kwargs):
        temp_args = {
            'metadata': render_template(self.metadata_template,
                                        **self.metadata),
            'site_metadata': self.metadata['site'],
            'uuid': self.metadata['uuid'],
            'data_type': self.data_type,
        }
        return temp_args

    def get(self, uuid):
        """Presents a delete confirmation to the user"""
        metadata_request = self.api_handle.get_metadata(uuid)
        if metadata_request.status_code != 200:
            abort(404)
        self.metadata = metadata_request.json()
        self.metadata['uuid'] = uuid
        self.metadata['site'] = self.get_site_metadata(
            self.metadata['site_id'])
        return render_template(
            self.template,
            **self.template_args(**self.metadata))

    def post(self, uuid):
        delete_request = self.api_handle.delete(uuid)
        if delete_request.status_code != 204:
            abort(404)
        return redirect(url_for(f'data_dashboard.{self.data_type}s'))

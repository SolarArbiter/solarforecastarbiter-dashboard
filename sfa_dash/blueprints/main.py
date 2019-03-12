import pdb
from sfa_dash.blueprints.dash import DataDashView
from sfa_dash.blueprints.data_listing import DataListingView
from sfa_dash.blueprints.sites import SingleSiteView, SitesListingView
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables
from sfa_dash.api_interface import observations, forecasts
from sfa_dash.api_interface import demo_data
from flask import (Flask, Blueprint, render_template,
                   request, url_for, redirect)
from flask.views import MethodView                  


class SingleObservationView(DataDashView):
    template = 'data/asset.html'

    def make_breadcrumb_html(self, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = ''
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.sites_view'),
            text='Sites')
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.site_view',
                        site_id=self.metadata['site_id']),
	    text=self.metadata['site']['name'])
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.observations',
                        site_id=self.metadata['site_id']),
            text='Observations')
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.observation_data',
                        obs_id=self.metadata['obs_id']),
            text=self.metadata['name'])
        return breadcrumb


    def get(self, obs_id, **kwargs):
        self.metadata = observations.get_metadata(obs_id)
        temp_args = self.template_args(**kwargs)
        site_link = url_for('data_dashboard.site_view',
                            site_id=self.metadata['site_id'])
        self.metadata['site_link'] = f'<a href="{site_link}">{self.metadata["site"]["name"]}</a>'
        temp_args['metadata'] = render_template('data/metadata/observation_metadata.html',
                                                **self.metadata)
        temp_args['upload_link'] = '/demo/obs_upload'
        return render_template(self.template, **temp_args)


class SingleForecastView(DataDashView):
    template = 'data/asset.html'

    def make_breadcrumb_html(self, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = ''
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.sites_view'),
            text='Sites')
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.site_view',
                        site_id=self.metadata['site_id']),
	    text=self.metadata['site']['name'])
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.forecasts',
                        site_id=self.metadata['site_id']),
            text='Forecasts')
        breadcrumb += breadcrumb_format.format(
            url=url_for('data_dashboard.forecast_data',
                        forecast_id=self.metadata['forecast_id']),
            text=self.metadata['name'])
        return breadcrumb


    def get(self, forecast_id, **kwargs):
        self.metadata = forecasts.get_metadata(forecast_id)
        temp_args = self.template_args(**kwargs)
        site_link = url_for('data_dashboard.site_view',
                            site_id=self.metadata['site_id'])
        self.metadata['site_link'] = f'<a href="{site_link}">{self.metadata["site"]["name"]}</a>'
        temp_args['metadata'] = render_template('data/metadata/forecast_metadata.html', **self.metadata)
        temp_args['upload_link'] = '/demo/fx_upload'
        return render_template(self.template, **temp_args)


class AccessView(DataDashView):
    template = 'data/access.html'


class ReportsView(DataDashView):
    template = 'data/reports.html'


class TrialsView(DataDashView):
    template = 'data/trials.html'


class ToSites(MethodView):
    def get(self):
        return redirect('/sites', 302)

data_dash_blp = Blueprint('data_dashboard', 'data_dashboard')
data_dash_blp.add_url_rule('/sites/', view_func=SitesListingView.as_view('sites_view'))
data_dash_blp.add_url_rule('/sites/<site_id>/', view_func=SingleSiteView.as_view('site_view'))
data_dash_blp.add_url_rule('/sites/<site_id>/<name>/access', view_func=AccessView.as_view('observation_named_access'))
data_dash_blp.add_url_rule('/sites/<site_id>/<name>/reports', view_func=ReportsView.as_view('observation_named_reports'))
data_dash_blp.add_url_rule('/sites/<site_id>/<name>/trials', view_func=TrialsView.as_view('observation_named_trials'))
data_dash_blp.add_url_rule('/observations/', view_func=DataListingView.as_view('observations', data_type='observation'))
data_dash_blp.add_url_rule('/observations/<obs_id>', view_func=SingleObservationView.as_view('observation_data'))
data_dash_blp.add_url_rule('/forecasts/', view_func=DataListingView.as_view('forecasts', data_type='forecast'))
data_dash_blp.add_url_rule('/forecasts/<forecast_id>', view_func=SingleForecastView.as_view('forecast_data'))

#Temporary redirect to sites page
data_dash_blp.add_url_rule('/', view_func=ToSites.as_view('root_redirect'))

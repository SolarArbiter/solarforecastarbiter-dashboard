import pdb
from sfa_dash.blueprints.dash import DataDashView
from sfa_dash.blueprints.data_assets import DataListingView
from sfa_dash.blueprints.site import SingleSiteView
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables
from sfa_dash.api_interface.requests import api_get
from sfa_dash.api_interface import demo_data
from flask import Flask, Blueprint, render_template, request, url_for



class DataView(DataDashView):
    template = 'data/asset.html'

    def make_breadcrumb_html(self, site=None, organization=None, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = ''
        breadcrumb += breadcrumb_format.format(
                        url='/sites',
                        text='Sites')
        breadcrumb += breadcrumb_format.format(
                        url='/sites/Ashland%20OR',
	                text='Ashland OR')
        breadcrumb += breadcrumb_format.format(
            url='/observations?site=Ashland%20OR',
            text='Observations')
        breadcrumb += breadcrumb_format.format(
            url='/observations/123e4567-e89b-12d3-a456-426655440000',
            text='Ashland OR, ghi')
        return breadcrumb


    def get(self, **kwargs):
        temp_args = self.template_args(**kwargs)
        metadata = demo_data.observation #api_get('/observations/station/metadata')
        temp_args['metadata'] = render_template('data/metadata/observation_metadata.html', **metadata)
        # TODO: get data from api, generate bokeh plots
        return render_template(self.template, **temp_args)


class AccessView(DataDashView):
    template = 'data/access.html'


class ReportsView(DataDashView):
    template = 'data/reports.html'


class TrialsView(DataDashView):
    template = 'data/trials.html'


class OrgView(BaseView):
    template = 'org/obs.html'
    subnav_format = {
        '{observations_url}': 'Observation Data',
        '{forecasts_url}': 'Forecast Data',
        '{trials_url}': 'Trials',
    }
    
    def template_args(self, organization, **kwargs):
        subnav_kwargs = {
            'observations_url': url_for('data_dashboard.observations', organization=organization),
            ## TODO: Set these to trials & forecasts
            'forecasts_url': url_for('data_dashboard.forecasts', organization=organization),
            'trials_url': url_for('data_dashboard.observations', organization=organization),
        }
        return {'breadcrumb': self.make_breadcrumb_html(),
                'current_path': request.path,
                'subnav': self.format_subnav(**subnav_kwargs)}


    def get(self, **kwargs):
        temp_args = self.template_args(**kwargs)
        temp_args['data_table'] = DataTables.get_observation_table(**kwargs)
        return render_template(self.template, **temp_args) 


data_dash_blp = Blueprint('data_dashboard', 'data_dashboard')
data_dash_blp.add_url_rule('/<organization>', view_func=OrgView.as_view('organization_view'))
data_dash_blp.add_url_rule('/sites/', view_func=DataListingView.as_view('sites_view', data_type='sites'))
data_dash_blp.add_url_rule('/sites/<site_id>/', view_func=SingleSiteView.as_view('site_view'))
data_dash_blp.add_url_rule('/sites/<site>/<name>', view_func=DataView.as_view('observation_named_data'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/access', view_func=AccessView.as_view('observation_named_access'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/reports', view_func=ReportsView.as_view('observation_named_reports'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/trials', view_func=TrialsView.as_view('observation_named_trials'))
data_dash_blp.add_url_rule('/observations/', view_func=DataListingView.as_view('observations', data_type='observations'))
data_dash_blp.add_url_rule('/forecasts/', view_func=DataListingView.as_view('forecasts', data_type='forecasts'))


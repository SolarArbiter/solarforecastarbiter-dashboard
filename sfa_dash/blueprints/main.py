import pdb
from sfa_dash.blueprints.dash import DataDashView
from sfa_dash.blueprints.data_assets import DataListingView
from sfa_dash.blueprints.site import SingleSiteView
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables
from sfa_dash.api_interface.requests import api_get
from sfa_dash.api_interface import demo_data
from flask import (Flask, Blueprint, render_template,
                   request, url_for, redirect)
from flask.views import MethodView                  



class DataView(DataDashView):
    template = 'data/asset.html'

    def make_breadcrumb_html(self, **kwargs):
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
            text=kwargs['name'])
        return breadcrumb


    def get(self, **kwargs):
        temp_args = self.template_args(**kwargs)
        metadata = demo_data.observation #api_get('/observations/station/metadata')
        metadata['site_link'] = f'<a href="/sites/{metadata["site"]["name"]}">{metadata["site"]["name"]}</a>'
        temp_args['metadata'] = render_template('data/metadata/observation_metadata.html', **metadata)
        temp_args['upload_link'] = '/demo/obs_upload'
        # TODO: get data from api, generate bokeh plots
        return render_template(self.template, **temp_args)


class TempDataView(DataDashView):
    template = 'data/asset.html'

    def make_breadcrumb_html(self, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = ''
        breadcrumb += breadcrumb_format.format(
                        url='/sites',
                        text='Sites')
        breadcrumb += breadcrumb_format.format(
                        url='/sites/Power%20Plant%201',
	                text='Power Plant 1')
        breadcrumb += breadcrumb_format.format(
            url='/forecasts?site=Power%20Plant%201',
            text='Forecasts')
        breadcrumb += breadcrumb_format.format(
            url=f'/forecasts/{kwargs["name"]}',
            text=kwargs['name'])
        return breadcrumb


    def get(self, **kwargs):
        temp_args = self.template_args(**kwargs)
        metadata = demo_data.forecast
        metadata['site_link'] = f'<a href="/sites/{metadata["site"]["name"]}">{metadata["site"]["name"]}</a>'
        temp_args['metadata'] = render_template('data/metadata/forecast_metadata.html', **metadata)
        temp_args['upload_link'] = '/demo/fx_upload'
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

class ToSites(MethodView):
    def get(self):
        return redirect('/sites', 302)

#data_dash_blp.add_url_rule('/<organization>', view_func=OrgView.as_view('organization_view'))
data_dash_blp = Blueprint('data_dashboard', 'data_dashboard')
data_dash_blp.add_url_rule('/sites/', view_func=DataListingView.as_view('sites_view', data_type='sites'))
data_dash_blp.add_url_rule('/sites/<site_id>/', view_func=SingleSiteView.as_view('site_view'))
data_dash_blp.add_url_rule('/sites/<site>/<name>', view_func=DataView.as_view('observation_named_data'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/access', view_func=AccessView.as_view('observation_named_access'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/reports', view_func=ReportsView.as_view('observation_named_reports'))
data_dash_blp.add_url_rule('/sites/<site>/<name>/trials', view_func=TrialsView.as_view('observation_named_trials'))
data_dash_blp.add_url_rule('/observations/', view_func=DataListingView.as_view('observations', data_type='observations'))
data_dash_blp.add_url_rule('/forecasts/', view_func=DataListingView.as_view('forecasts', data_type='forecasts'))
data_dash_blp.add_url_rule('/forecasts/<name>', view_func=TempDataView.as_view('forecast_data'))

#Temporary redirect to sites page
data_dash_blp.add_url_rule('/', view_func=ToSites.as_view('root_redirect'))


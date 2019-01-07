import pdb
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables
from sfa_dash.api_interface.requests import api_get
from flask import Flask, Blueprint, render_template, request, url_for


class DataListingView(BaseView):
    """Lists accessible forecasts/observations. Includes 
    """
    template = 'org/obs.html'
    subnav_format = {
        '{observations_url}': 'Observations',
        '{forecasts_url}': 'Forecasts',
        '{trials_url}': 'Trials',
    }

    def __init__(self, data_type, **kwargs):
        """
        """
        if data_type == 'forecasts':
            self.table_function = DataTables.get_forecast_table
        elif data_type == 'observations':
            self.table_function = DataTables.get_observation_table
        elif data_type == 'sites':
            self.table_function = DataTables.get_site_table
        else:
            # 
            raise Exception
        self.data_type = data_type
    

    def breadcrumb_html(self, site=None, organization=None, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = ''
        if organization is not None:
            breadcrumb = breadcrumb_format.format(
                            url=url_for('data_dashboard.organization_view', organization=organization),
                            text=organization)
        #pdb.set_trace()
        if site is not None:
            breadcrumb += breadcrumb_format.format(
                            url='/sites',
                            text='Sites')
            breadcrumb += breadcrumb_format.format(
                            url='/sites',# TODO: get site_id for this url_for('data_dashboard.site_view'),
                            text=site)
        breadcrumb += breadcrumb_format.format(
            url='/'+self.data_type,
            text=self.data_type.capitalize())
        return breadcrumb


    def get_template_args(self, **kwargs):
        """Create a dictionary containing the required arguments for the template
        """
        template_args = {}
        subnav_kwargs = {
            'observations_url': url_for('data_dashboard.observations', **kwargs),
            'forecasts_url': url_for('data_dashboard.forecasts', **kwargs),
            'trials_url': url_for('data_dashboard.observations', **kwargs),
        }
        template_args['subnav'] = self.format_subnav(**subnav_kwargs)
        template_args['data_table'] = self.table_function(**kwargs)
        template_args['current_path'] = request.path
        template_args['breadcrumb'] = self.breadcrumb_html(**kwargs)
        return template_args

    def get(self, **kwargs):
        """
        """
        # if organization query parameter, add it to the breadcrumb
        # query api
        # render table of observations
        if request.args.get('organization') is not None:
            kwargs.update({'organization': request.args.get('organization')})
        if request.args.get('site') is not None:
            kwargs.update({'site': request.args.get('site')})
        return render_template(self.template, **self.get_template_args(**kwargs))

import pdb
"""Flask endpoints for listing Observations, Forecasts and CDF Forecasts.
Defers actual table creation and rendering to DataTables in the util module.
"""
from collections import OrderedDict
from flask import render_template, request, url_for


from sfa_dash.api_interface import sites
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables, handle_response
from sfa_dash.filters import human_friendly_datatype

from sfa_dash.errors import DataRequestException


class DataListingView(BaseView):
    """Lists accessible forecasts/observations.
    """
    template = 'org/obs.html'
    subnav_format = {
        '{observations_url}': 'Observations',
        '{forecasts_url}': 'Forecasts',
        '{cdf_forecasts_url}': 'Probabilistic Forecasts',
    }

    def __init__(self, data_type, **kwargs):
        """
        """
        if data_type == 'forecast':
            self.table_function = DataTables.get_forecast_table
        elif data_type == 'observation':
            self.table_function = DataTables.get_observation_table
        elif data_type == 'cdf_forecast_group':
            self.table_function = DataTables.get_cdf_forecast_table
        else:
            raise Exception
        self.data_type = data_type

    def get_breadcrumb_dict(self, **kwargs):
        """Build the breadcrumb dictionary for the listing page. Depends on properly
        formatted kwargs.
        """
        breadcrumb_dict = OrderedDict()
        human_label = human_friendly_datatype(self.data_type)       
        if 'site_id' in kwargs:
            breadcrumb_dict['Sites'] = url_for('data_dashboard.sites')
            breadcrumb_dict['Site name here!'] = url_for('data_dashboard.site_view',
                                                         uuid=kwargs['site_id'])
        elif 'aggregate_id' in kwargs:
            breadcrumb_dict['Aggregates'] = url_for('data_dashboard.aggregates')
            breadcrumb_dict['Aggregate name here!'] = url_for('data_dashboard.aggregate_view',
                                                              uuid=kwargs['aggregate_id'])
        breadcrumb_dict[f'{human_label}s'] = url_for(f'data_dashboard.{self.data_type}s',
                                                      **kwargs)
        return breadcrumb_dict
        
    def get_template_args(self, **kwargs):
        """Create a dictionary containing the required arguments for the template
        """
        template_args = {}
        subnav_kwargs = {
            'observations_url': url_for('data_dashboard.observations',
                                        **kwargs),
            'forecasts_url': url_for('data_dashboard.forecasts',
                                     **kwargs),
            'cdf_forecasts_url': url_for('data_dashboard.cdf_forecast_groups',
                                         **kwargs)
        }
        template_args['subnav'] = self.format_subnav(**subnav_kwargs)
        template_args['data_table'] = self.table_function(**kwargs)
        template_args['current_path'] = request.path
        # If kwargs is not empty, a site_id or aggregate_id was passed
        if kwargs:
            template_args['breadcrumb'] = self.breadcrumb_html(self.get_breadcrumb_dict(**kwargs))
        else:
            template_args['page_title'] = 'Forecasts and Observations'
        return template_args

    def get(self):
        """
        """
        # Check for a uuid parameter indicating we should filter by site.
        # otherwise, set the create key to pass as a query parameter to
        # the site listing page.
        template_kwargs = {}
        if 'site_id' in request.args:
            template_kwargs.update({'site_id': request.args.get('site_id')})
        elif 'aggregate_id' in request.args:
            template_kwargs.update({'aggregate_id': request.args.get('aggregate_id')})
        try:
            temp_args = self.get_template_args(**template_kwargs)
        except DataRequestException as e:
            temp_args = {'errors': e.errors}
        return render_template(self.template, **temp_args)

"""Flask endpoints for listing Observations, Forecasts and CDF Forecasts.
Defers actual table creation and rendering to DataTables in the util module.
"""
from collections import OrderedDict
from flask import render_template, request, url_for


from sfa_dash.api_interface import sites, aggregates
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
        """Build the breadcrumb dictionary for the listing page. If site_id
        or aggregate_id are passed as key word arguments, prepends the
        appropriate links. Note that these links depend on the existence of
        the self.location_data attribute, that should only be set by during
        a successful fetch of the site/aggregates metadata.
        """
        breadcrumb_dict = OrderedDict()
        human_label = human_friendly_datatype(self.data_type)
        if 'site_id' in kwargs:
            breadcrumb_dict['Sites'] = url_for('data_dashboard.sites')
            breadcrumb_dict[self.location_data['name']] = url_for(
                'data_dashboard.site_view', uuid=kwargs['site_id'])
        elif 'aggregate_id' in kwargs:
            breadcrumb_dict['Aggregates'] = url_for(
                'data_dashboard.aggregates')
            breadcrumb_dict[self.location_data['name']] = url_for(
                'data_dashboard.aggregate_view', uuid=kwargs['aggregate_id'])
        breadcrumb_dict[f'{human_label}s'] = url_for(
            f'data_dashboard.{self.data_type}s', **kwargs)
        return breadcrumb_dict

    def get_subnav_kwargs(self, **kwargs):
        """Creates a dict to be used when formating the sub navigation. The
        resulting dict is used to format the fstring keys found in the
        DataListingView.subnav_format variable.
        """
        subnav_kwargs = {}
        if 'aggregate_id' in kwargs:
            subnav_kwargs['observations_url'] = url_for(
                'data_dashboard.aggregate_view', uuid=kwargs['aggregate_id'])
        else:
            subnav_kwargs['observations_url'] = url_for(
                'data_dashboard.observations', **kwargs)
        subnav_kwargs['forecasts_url'] = url_for(
            'data_dashboard.forecasts', **kwargs)
        subnav_kwargs['cdf_forecasts_url'] = url_for(
            'data_dashboard.cdf_forecast_groups', **kwargs)
        return subnav_kwargs

    def get_template_args(self, **kwargs):
        """Create a dictionary containing the required arguments for the
        template. Special keyword arguments of `site_id` or `aggregate_id` can
        be passed to filter results by a site or aggregate.
        """
        template_args = {}
        template_args['subnav'] = self.format_subnav(
            **self.get_subnav_kwargs(**kwargs))
        template_args['data_table'] = self.table_function(**kwargs)
        template_args['current_path'] = request.path
        # If kwargs is not empty, a site_id or aggregate_id was passed
        if kwargs:
            template_args['breadcrumb'] = self.breadcrumb_html(
                self.get_breadcrumb_dict(**kwargs))
        else:
            template_args['page_title'] = 'Forecasts and Observations'
        return template_args

    def get(self):
        """
        """
        # Check for a site id or aggregate id in the query parameters.If found,
        # sets location_id and api_handle to later request metadata of the site
        # or aggregate and adds the id to a key word argument dict to be passed
        # to other setup functions.
        template_kwargs = {}
        if 'site_id' in request.args:
            location_id = request.args.get('site_id')
            api_handle = sites
            template_kwargs.update({'site_id': location_id})
        elif 'aggregate_id' in request.args:
            location_id = request.args.get('aggregate_id')
            template_kwargs.update({'aggregate_id': location_id})
            api_handle = aggregates
        else:
            api_handle = None
        try:
            if api_handle:
                self.location_data = handle_response(
                    api_handle.get_metadata(location_id))
            temp_args = self.get_template_args(**template_kwargs)
        except DataRequestException as e:
            temp_args = {'errors': e.errors}
        return render_template(self.template, **temp_args)

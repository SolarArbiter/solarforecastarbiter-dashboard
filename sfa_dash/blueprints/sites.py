from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import DataTables
from sfa_dash.blueprints.dash import SiteDashView
from sfa_dash.blueprints.data_listing import DataListingView
from sfa_dash.api_interface import demo_data, sites
from flask import Flask, Blueprint, render_template, url_for, request


class SitesListingView(SiteDashView):
    template = 'org/obs.html'

    def breadcrumb_html(self, site=None, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = breadcrumb_format.format(
            url=url_for('data_dashboard.sites_view'),
            text='Sites')
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
        template_args['data_table'] = DataTables.get_site_table(**kwargs)
        template_args['current_path'] = request.path
        template_args['breadcrumb'] = self.breadcrumb_html(**kwargs)
        return template_args


    def get(self, **kwargs):
        return render_template(self.template, **self.get_template_args(**kwargs))


class SingleSiteView(SiteDashView):
    template = 'data/site.html'


    def make_breadcrumb_html(self, **kwargs):
        bc_format = '/<a href="{url}">{text}</a>'
        bc = ''
        bc += bc_format.format(
                url=url_for('data_dashboard.sites_view'),
                text="Sites")
        bc += bc_format.format(
                url=url_for('data_dashboard.site_view',
                            site_id=self.metadata['site_id']),
                text=self.metadata['name'])
        return bc


    def get(self, site_id, **kwargs):
        self.metadata = sites.get_metadata(site_id)
        return render_template(self.template, **self.template_args(**kwargs))

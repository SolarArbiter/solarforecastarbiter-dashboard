import json
from sfa_dash.blueprints.util import DataTables
from sfa_dash.blueprints.dash import SiteDashView
from sfa_dash.api_interface import sites, climate_zones
from sfa_dash.errors import DataRequestException
from flask import render_template, url_for, request


class SitesListingView(SiteDashView):
    """Render a page with a table listing Sites.
    """
    template = 'data/table.html'

    def breadcrumb_html(self, site=None, **kwargs):
        breadcrumb_format = '/<a href="{url}">{text}</a>'
        breadcrumb = breadcrumb_format.format(
            url=url_for('data_dashboard.sites'),
            text='Sites')
        return breadcrumb

    def get_climate_zone_data(self):
        """Create a dict of climate zone geojson data.
        """
        all_zones = climate_zones.get_zones()
        for zone in all_zones:
            zone.pop('_links')
            try:
                geo_data = climate_zones.get_zone_geojson(zone['name'])
            except DataRequestException as e:
                self.flash_api_errors(e.errors)
                zone['geojson'] = None
            else:
                zone['geojson'] = json.loads(geo_data)
        return all_zones

    def set_template_args(self):
        """Create a dictionary containing the required arguments for the template
        """
        self.template_args = {}
        table, site_data = DataTables.get_site_table()
        self.template_args['data_table'] = table
        self.template_args['current_path'] = request.path
        self.template_args['breadcrumb'] = self.breadcrumb_html()
        zone_data = self.get_climate_zone_data()
        # pop extra params to ensure valid json is passed to page_data
        for site in site_data:
            site.pop('extra_parameters')
        self.template_args['page_data'] = {
            'climate_zones': zone_data,
            'sites': site_data,
        }

    def get(self):
        try:
            self.set_template_args()
        except DataRequestException as e:
            return render_template(self.template, errors=e.errors)
        return render_template(self.template, **self.template_args)


class SingleSiteView(SiteDashView):
    """Render a page to display the metadata of a a single Site.
    """
    template = 'data/site.html'

    def breadcrumb_html(self, **kwargs):
        bc_format = '/<a href="{url}">{text}</a>'
        bc = ''
        bc += bc_format.format(
            url=url_for('data_dashboard.sites'),
            text="Sites")
        bc += bc_format.format(
            url=url_for('data_dashboard.site_view',
                        uuid=self.metadata['site_id']),
            text=self.metadata['name'])
        return bc

    def get(self, uuid, **kwargs):
        try:
            self.metadata = sites.get_metadata(uuid)
        except DataRequestException as e:
            return render_template(self.template, errors=e.errors)
        self.set_template_args(**kwargs)
        return render_template(self.template, **self.template_args)

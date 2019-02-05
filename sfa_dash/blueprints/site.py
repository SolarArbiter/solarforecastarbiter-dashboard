import pdb
from sfa_dash.blueprints.dash import SiteDashView
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.data_assets import DataListingView
from sfa_dash.api_interface.requests import api_get
from sfa_dash.api_interface import demo_data
from flask import Flask, Blueprint, render_template, url_for


class SingleSiteView(SiteDashView):
    template = 'data/site.html'
    def make_breadcrumb_html(self, **kwargs):
        bc_format = '/<a href="{url}">{text}</a>'
        bc = ''
        bc += bc_format.format(
                url="/sites",
                text="Sites")
        bc += bc_format.format(
                url="/sites/{}".format(self.site_id),
                text=self.site_id)
        return bc


    def create_table_elements(self, data_list, id_key, **kwargs):
        table_rows = []
        for data in data_list:
            table_row = {}
            site_name = data['site']['name']
            #TODO: replace organization with api-provided value
            organization = "TEP"
            table_row['name'] = data['name']
            table_row['variable'] = data['variable']
            table_row['uuid'] = data[id_key]
            table_row['link'] = url_for("data_dashboard.observation_named_data",
                                        organization=organization,
                                        name=data['name'],
                                        site=site_name)
            table_rows.append(table_row)
        return table_rows

    def get(self, site_id, **kwargs):
        kwargs['organization'] = "TEP"
        if site_id == 'SOLRMAP University of Arizona (OASIS)':
            data = demo_data.site_1
        elif site_id == 'Power Plant 1':
            data = demo_data.site_2
        else:
            data = demo_data.site
        self.site_id = site_id
        metadata = data #api_get('/sites/123e4567-e89b-12d3-a456-426655440001')
        kwargs.update({'site': metadata['name']})
        kwargs.update(metadata)
        temp_args = self.template_args(**kwargs)
        temp_args['metadata'] = render_template('data/metadata/site_metadata.html', **metadata)
        obs_data = demo_data.observations# api_get('/sites/123e4567-e89b-12d3-a456-426655440001/observations')
        rows = self.create_table_elements(obs_data, 'obs_id', **kwargs)
        #temp_args['listing'] = render_template('data/table/observation_table.html', table_rows=rows)
        return render_template(self.template, **temp_args)

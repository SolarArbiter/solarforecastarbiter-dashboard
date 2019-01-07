""" Utility classes/functions. Mostly for handling api data.
"""
from sfa_dash.api_interface.requests import api_get
from sfa_dash.api_interface import demo_data
from flask import render_template, url_for


class DataTables(object):
    observation_template = 'data/table/observation_table.html'
    forecast_template = 'data/table/forecast_table.html'
    site_template = 'data/table/site_table.html'

    @classmethod
    def create_table_elements(cls, data_list, id_key, organization=None, **kwargs):
        """Creates a list of objects to be rendered as table by jinja template
        """
        table_rows = []
        for data in data_list:
            table_row = {}
            site_name = data['site']['name']
            table_row['name'] = data['name']
            table_row['variable'] = data['variable']
            table_row['provider'] = data['provider']
            table_row['uuid'] = data[id_key]
            table_row['link'] = url_for('data_dashboard.observation_named_data',
                                        organization=organization,
                                        name=data['name'],
                                        site=site_name)
            table_rows.append(table_row)
        return table_rows  


    @classmethod
    def create_site_table_elements(cls, data_list, id_key, **kwargs):
        table_rows = []
        for data in data_list:
            table_row = {}
            table_row['name'] = data['name']
            table_row['provider'] = data['provider']
            table_row['uuid'] = data[id_key]
            table_row['link'] = url_for("data_dashboard.site_view",
                                        site_id=data['name'])
            table_rows.append(table_row)
        return table_rows


    @classmethod
    def get_observation_table(cls, **kwargs):
        """Returns a rendered observation table.
        TODO: fix parameters.
        """
        obs_data = demo_data.observations
        rows = cls.create_table_elements(obs_data, 'obs_id', **kwargs)
        rendered_table = render_template(cls.observation_template, table_rows=rows)
        return rendered_table


    @classmethod
    def get_forecast_table(cls, **kwargs):
        """
        """
        forecast_data = demo_data.forecasts
        #forecast_data = api_get('/forecasts/')
        rows = cls.create_table_elements(forecast_data, 'forecast_id', **kwargs)
        rendered_table = render_template(cls.forecast_template, table_rows=rows)
        return rendered_table

    @classmethod
    def get_site_table(cls, **kwargs):
        """
        """
        site_data = demo_data.sites
        rows = cls.create_site_table_elements(site_data, 'site_id', **kwargs)
        rendered_table = render_template(cls.site_template, table_rows=rows)
        return rendered_table

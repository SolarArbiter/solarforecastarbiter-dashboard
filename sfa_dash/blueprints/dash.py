"""Dashboards are wrappers providing navigation and contextual content based on site-section.
"""
import pdb
from sfa_dash.blueprints.base import BaseView
from flask import Flask, Blueprint, render_template, request, url_for


class DataDashView(BaseView):
    subnav_format = {}
    def template_args(self, **kwargs):
         temp_args = {}
         temp_args['current_path'] = request.path
         temp_args['subnav'] = self.format_subnav(**kwargs)
         temp_args['breadcrumb'] = self.make_breadcrumb_html(**kwargs)
         return temp_args


    def get(self, **kwargs):
        return render_template(self.template, **self.template_args(**kwargs))


class SiteDashView(BaseView):
    template = 'data/site.html'
    subnav_format = {
        '{observations_url}': 'Observations',
        '{forecasts_url}': 'Forecasts',
    }
    def template_args(self, **kwargs):
         """
         """
         temp_args = {}
         subnav_kwargs = {
            'forecasts_url': url_for('data_dashboard.forecasts', site_id=self.metadata['site_id']),
            'observations_url': url_for('data_dashboard.observations', site_id=self.metadata['site_id']),
         }
         temp_args['subnav'] = self.format_subnav(**subnav_kwargs)
         temp_args['breadcrumb'] = self.make_breadcrumb_html()
         temp_args['metadata'] = render_template('data/metadata/site_metadata.html', **self.metadata)
         temp_args['site_id'] = self.metadata['site_id']
         return temp_args



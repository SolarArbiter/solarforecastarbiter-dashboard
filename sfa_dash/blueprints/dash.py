"""Dashboards are wrappers providing navigation and contextual content based on site-section.
"""
import pdb
from sfa_dash.blueprints.base import BaseView
from flask import Flask, Blueprint, render_template, request, url_for


class DataDashView(BaseView):
    subnav_format = {}
    #     "/{organization}/{site}/{name}": "Data",
    #     "/{organization}/{site}/{name}/access": "Access",
    #     "/{organization}/{site}/{name}/trials": "Active Trials",
    #     "/{organization}/{site}/{name}/reports": "Reports",
    # }
    def template_args(self, **kwargs):
         temp_args = {}
         temp_args['current_path'] = request.path
         temp_args['subnav'] = self.format_subnav(**kwargs)
         temp_args['breadcrumb'] = self.make_breadcrumb_html()
         return temp_args


    def get(self, **kwargs):
        return render_template(self.template, **self.template_args(**kwargs))


class SiteDashView(BaseView):
    template = 'data/site.html'
    subnav_format = {
        '{forecasts_url}': 'Forecasts',
        '{observations_url}': 'Observations',
    }
    def template_args(self, **kwargs):
         """
         """
         temp_args = {}
         subnav_kwargs = {
            'forecasts_url': url_for('data_dashboard.forecasts', site=kwargs['site']),
            'observations_url': url_for('data_dashboard.observations', site=kwargs['site']),
         }
         temp_args['subnav'] = self.format_subnav(**subnav_kwargs)
         temp_args['breadcrumb'] = self.make_breadcrumb_html()
         return temp_args


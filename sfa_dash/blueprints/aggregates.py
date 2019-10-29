from collections import OrderedDict

from flask import render_template, url_for

from solarforecastarbiter.reports.main import report_to_html_body
from sfa_dash.api_interface import observations, forecasts, sites, aggregates
from sfa_dash.blueprints.base import BaseView
from sfa_dash.blueprints.util import filter_form_fields, handle_response


class AggregatesView(BaseView):
    template = 'dash/aggregates.html'


    def get_breadcrumb_dict(self):
        breadcrumb_dict = OrderedDict()
        breadcrumb_dict['Aggregates'] = url_for('data_dashboard.aggregates')
        return breadcrumb_dict

    def template_args(self):
        aggregates_list = handle_response(aggregates.list_metadata())
        return {
            "breadcrumb": self.breadcrumb_html(self.get_breadcrumb_dict()),
            "aggregates": aggregates_list,
        }

class AggregateForm(BaseView):
    template = 'forms/aggregate_form.html'

    def template_args(self):
        return {'page_data': {}}


    def post(self):
        return "Not done yet!"


class AggregateView(BaseView):
    template = 'data/aggregate.html'
    metadata_template = 'data/metadata/aggregate_metadata.html'
    
    def get_breadcrumb_dict(self):
        breadcrumb_dict = OrderedDict()
        breadcrumb_dict['Aggregates'] = url_for('data_dashboard.aggregates')
        breadcrumb_dict[self.metadata['name']] = url_for(
            'data_dashboard.aggregate_view',
            uuid=self.metadata['aggregate_id'])
        return breadcrumb_dict

    def template_args(self):
        return {
            'metadata': render_template(
                self.metadata_template,
                metadata_object=self.metadata),
            'observations': self.observation_list,
            'breadcrumb': self.breadcrumb_html(
                self.get_breadcrumb_dict()),
        }

    def get(self, uuid):
        self.metadata = handle_response(aggregates.get_metadata(uuid))
        self.observation_list= []
        observations_list = handle_response(observations.list_metadata())
        observation_dict = {obs['observation_id']: obs
                            for obs in observations_list}
        for obs_id in [obs['observation_id'] for obs in self.metadata['observations']]:
            if obs_id in observation_dict:
                self.observation_list.append(observation_dict[obs_id])
        return super().get()


class DeleteAggregateView(BaseView):
    def get(self):
        return "Not done yet!"

    def post(self):
        return "Not done yet!"

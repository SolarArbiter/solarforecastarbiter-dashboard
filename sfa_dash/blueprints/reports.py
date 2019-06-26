"""Draft of reports endpoints/pages. Need to integrate core report generation.
"""
import json
from flask import request, redirect, url_for, abort
import pandas as pd

from sfa_dash.api_interface import observations, forecasts, reports
from sfa_dash.blueprints.base import BaseView


class ReportsView(BaseView):
    template = 'dash/reports.html'

    def template_args(self):
        reports_req = reports.list_metadata()
        reports_list = reports_req.json()
        return {
            "page_title": 'Reports',
            "reports": reports_list,
        }


class ReportForm(BaseView):
    template = 'forms/report_form.html'

    def parse_extra_parameters(self, with_params):
        try:
            params = json.loads(with_params['extra_parameters'])
        except json.decoder.JSONDecodeError:
            params = {}
        with_params.update({
            'extra_parameters': params,
        })

    def get_pairable_objects(self):
        """Requests the forecasts and observations from
        the api for injecting into the dom as a js variable
        """
        observation_request = observations.list_metadata()
        forecast_request = forecasts.list_metadata()
        observation_list = observation_request.json()
        for obs in observation_list:
            self.parse_extra_parameters(obs)
        forecast_list = forecast_request.json()
        for fx in forecast_list:
            self.parse_extra_parameters(fx)
        return {
            'observations': observation_list,
            'forecasts': forecast_list,
        }

    def template_args(self):
        return {
            "form_title": "Create new Report",
            "page_data": self.get_pairable_objects(),
        }

    def field_values(self, prefix, form_data):
        """Return a list of values of form elements where the name atribute starts with
        prefix.
        """
        return [form_data[key]
                for key in form_data.keys()
                if key.startswith(prefix)]

    def zip_object_pairs(self, form_data):
        """Create a list of observation, forecast tuples from the the
        (observation-n, forecast-n) input elements inserted by
        report-handling.js
        """
        obs = self.field_values('observation-', form_data)
        fx = self.field_values('forecast-', form_data)
        pairs = list(zip(obs, fx))
        return pairs

    def parse_metrics(self, form_data):
        """Collect the keys (name attributes) of the form elements with a value
        attribute of metrics. These elements are checkbox inputs, and are only
        included in the form data when selected.
        """
        return [k for k, v in form_data.items() if v == 'metrics']

    def parse_filters(self, form_data):
        """Return an empty array until we know more about how we want
        to configure these filters
        """
        return []

    def dt_fields_to_iso(self, form_data, field_prefix):
        """Concatenates the values from a date and time field with a shared prefix
        and returns the iso 8601 represenation.
        """
        field_date = form_data[f"{field_prefix}-date"]
        field_time = form_data[f"{field_prefix}-time"]
        field_dt = pd.Timestamp(f'{field_date} {field_time}', tz='utc')
        return field_dt.isoformat()

    def parse_report_parameters(self, form_data):
        params = {}
        params['object_pairs'] = self.zip_object_pairs(form_data)
        params['metrics'] = self.parse_metrics(form_data)
        params['filters'] = self.parse_filters(form_data)
        params['start'] = self.dt_fields_to_iso(form_data, 'period-start')
        params['end'] = self.dt_fields_to_iso(form_data, 'period-end')
        return params

    def report_formatter(self, form_data):
        formatted = {}
        formatted['name'] = form_data['name']
        formatted['report_parameters'] = self.parse_report_parameters(
            form_data)
        return formatted

    def post(self):
        form_data = request.form
        api_payload = self.report_formatter(form_data)
        post_req = reports.post_metadata(api_payload)
        if post_req.status_code == 201:
            return redirect(url_for('data_dashboard.reports'))
        elif post_req.status_code == 400:
            # flatten error response to handle nesting
            errors = post_req.json()['errors']
            return super().get(form_data=form_data, errors=errors)
        elif post_req.status_code == 404:
            errors = {'error': ['Permission to create report denied.']}
        else:
            errors = {'error': ['An unrecoverable error occured.']}
        return super().get(form_data=form_data, errors=errors)


class ReportView(BaseView):
    template = 'data/report.html'

    def template_args(self):
        return {'report_metadata': self.metadata}

    def get(self, uuid):
        # TODO: use core to buid templates
        report_request = reports.get_metadata(uuid)
        if report_request.status_code == 200:
            self.metadata = report_request.json()
        else:
            abort(404)
        return super().get()

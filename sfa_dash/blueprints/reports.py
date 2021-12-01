from flask import (request, redirect, url_for, render_template, send_file,
                   current_app, flash)

from sfa_dash.api_interface import (observations, forecasts, sites, reports,
                                    aggregates, cdf_forecast_groups, users,
                                    cdf_forecasts)
from sfa_dash.blueprints.base import BaseView
from sfa_dash.errors import DataRequestException
from sfa_dash.filters import api_varname_to_units
from sfa_dash.form_utils import converters
from sfa_dash.utils import check_sign_zip
from solarforecastarbiter.datamodel import Report, RawReport
from solarforecastarbiter.io.utils import load_report_values
from solarforecastarbiter.reports.template import (
    get_template_and_kwargs, render_html, render_pdf)


ALLOWED_REPORT_TYPES = ['deterministic', 'probabilistic', 'event']


class ReportsView(BaseView):
    template = 'data/reports.html'

    def set_template_args(self):
        try:
            reports_list = reports.list_metadata()
        except DataRequestException as e:
            return {'errors': e.errors}
        try:
            all_actions = users.actions_on_type('reports')
        except DataRequestException:
            all_actions = {}
        for report in reports_list:
            report.update(
                {'actions': all_actions.get(report['report_id'], [])})
        self.template_args = {
            "page_title": 'Reports',
            "reports": reports_list,
        }


class ReportForm(BaseView):
    def set_template(self):
        if self.report_type == 'event':
            self.template = 'forms/event_report_form.html'
        elif self.report_type == 'probabilistic':
            self.template = 'forms/probabilistic_report_form.html'
        else:
            self.template = 'forms/report_form.html'
        self.converter = converters.ReportConverter

    def __init__(self, report_type):
        if report_type not in ALLOWED_REPORT_TYPES:
            raise ValueError('Invalid report_type.')
        else:
            self.report_type = report_type
            self.set_template()

    def get_pairable_objects(self):
        """Requests the forecasts and observations from
        the api for injecting into the dom as a js variable
        """
        observation_list = observations.list_metadata()
        if self.report_type == 'probabilistic':
            forecast_list = cdf_forecast_groups.list_metadata()
        else:
            forecast_list = forecasts.list_metadata()
        site_list = sites.list_metadata()
        aggregate_list = aggregates.list_metadata()
        for obs in observation_list:
            del obs['extra_parameters']
        for fx in forecast_list:
            del fx['extra_parameters']
        for site in site_list:
            del site['extra_parameters']
        for agg in aggregate_list:
            del agg['extra_parameters']
        return {
            'observations': observation_list,
            'forecasts': forecast_list,
            'sites': site_list,
            'aggregates': aggregate_list
        }

    def set_template_args(self, **kwargs):
        self.template_args = {
            "page_data": self.get_pairable_objects(),
            "report_type": self.report_type,
        }

    def post(self):
        form_data = request.form
        api_payload = self.converter.formdata_to_payload(form_data)
        if len(api_payload['report_parameters']['object_pairs']) == 0:
            errors = {
                'error': [('Must include at least 1 Forecast, Observation '
                           'pair.')],
            }
            return self.get(
                form_data=self.converter.payload_to_formdata(api_payload),
                errors=errors)
        try:
            report_id = reports.post_metadata(api_payload)
        except DataRequestException as e:
            if e.status_code == 404:
                errors = {
                    '404': [('You do not have permission to create '
                             'reports. You may need to request '
                             'permissions from your organization '
                             'administrator.')]
                }
            else:
                errors = e.errors
            return self.get(
                form_data=self.converter.payload_to_formdata(api_payload),
                errors=errors)
        return redirect(url_for(
            'data_dashboard.report_view',
            uuid=report_id,
        ))


def build_report(metadata):
    """Reorganizes report processed values into the propper place for
    plotting and creates a `solarforecastarbiter.datamodel.Report` object.
    """
    report = Report.from_dict(metadata)
    if metadata['raw_report'] is not None:
        raw_report = RawReport.from_dict(metadata['raw_report'])
        pfxobs = load_report_values(raw_report, metadata['values'])
        report = report.replace(raw_report=raw_report.replace(
            processed_forecasts_observations=pfxobs))
    return report


class ReportView(BaseView):
    template = 'data/report.html'

    def should_include_timeseries(self):
        """Determines if we should try to display a timeseries plot based on
        if the report is complete and the total number of points to plot.
        """
        if self.metadata['status'] != 'complete':
            return False
        raw_report = self.metadata['raw_report']
        pfxobs = raw_report['processed_forecasts_observations']
        total_data_points = 0

        seen_fx = []
        seen_obs = []
        seen_aggs = []
        for fxobs in pfxobs:
            fxobs_original = fxobs["original"]
            series_count = 0
            # Only count forecasts we haven't already seen
            fx = fxobs_original.get("forecast")
            if fx and fx["forecast_id"] not in seen_fx:
                # Check for probabilistic forecasts. Valid point count will
                # only be supplied for a single timeseries, so we need to
                # multiply by the number of constant values.
                if "constant_values" in fx:
                    series_count += len(fx["constant_values"])
                else:
                    series_count += 1
                seen_fx.append(fx["forecast_id"])

            # account for the observations or aggregates not already seen
            obs = fxobs_original.get("observation")
            if obs and obs["observation_id"] not in seen_obs:
                seen_obs.append(obs["observation_id"])
                series_count += 1
            agg = fxobs_original.get("aggregate")
            if agg and agg["aggregate_id"] not in seen_aggs:
                seen_aggs.append(agg["aggregate_id"])
                series_count += 1

            # determine total data points for the forecast, observation pair
            fxobs_data_points = fxobs['valid_point_count'] * series_count
            total_data_points = total_data_points + fxobs_data_points
        return total_data_points < current_app.config['REPORT_DATA_LIMIT']

    def set_template_args(self):
        include_timeseries = self.should_include_timeseries()
        report_object = build_report(self.metadata)
        report_template, report_kwargs = get_template_and_kwargs(
            report_object,
            request.url_root.rstrip('/'),
            include_timeseries,
            True
        )
        report_kwargs.update({
            'report_template': report_template,
            'dash_url': request.url_root.rstrip('/'),
            'include_metrics_toc': False,
            'metadata': {
                'report_parameters': self.metadata['report_parameters']},
        })
        report_status = self.metadata.get('status')

        # display a message about omitting timeseries
        if not include_timeseries and report_status == 'complete':
            download_link = url_for('data_dashboard.download_report_html',
                                    uuid=self.metadata['report_id'])
            flash(
                f"""<strong>Warning</strong> Too many timeseries points
                detected. To improve performance time series plots have
                been omitted from this report. You may download a copy
                of this report with the timeseries plots included:
                <a href="{download_link}">Download HTML Report.</a>""",
                'warning')
        elif not self.metadata['values'] and report_status == 'complete':
            flash('Could not load any time series values of observations '
                  'or forecasts. Timeseries and scatter plots will not '
                  'be included. You may require the `read_values` '
                  'permission on this report, or the included forecasts '
                  'and observations.',
                  'warning')
        self.template_args = report_kwargs

    def set_metadata(self, uuid):
        """Loads all necessary data for loading a
        `solarforecastarbiter.datamodel.Report` with processed forecasts and
        observations.
        """
        metadata = reports.get_metadata(uuid)
        metadata['report_parameters']['object_pairs'] = []
        self.metadata = metadata

    def get(self, uuid):
        try:
            self.set_metadata(uuid)
        except DataRequestException as e:
            return render_template(self.template, uuid=uuid, errors=e.errors)
        return super().get()


class DownloadReportView(ReportView):
    def __init__(self, format_, **kwargs):
        self.format_ = format_

    def get(self, uuid):
        try:
            self.set_metadata(uuid)
        except DataRequestException as e:
            errors = {'errors': e.errors}
            return ReportView().get(uuid, errors=errors)

        exclude_timeseries = 'exclude_timeseries' in request.args

        # don't do the work of making a report if the format is incorrect
        if self.format_ not in ('html', 'pdf'):
            raise ValueError(
                'Only html and pdf report downloads are currently supported')

        fname = self.metadata['report_parameters']['name'].replace(
                ' ', '_')
        report_object = build_report(self.metadata)
        # render to right format
        if self.format_ == 'html':
            bytes_out = render_html(
                report_object,
                request.url_root.rstrip('/'),
                with_timeseries=not exclude_timeseries, body_only=False
            ).encode('utf-8')
        elif self.format_ == 'pdf':
            bytes_out = render_pdf(
                report_object,
                request.url_root.rstrip('/'),
            )

        out = check_sign_zip(bytes_out, fname + f'.{self.format_}',
                             current_app.config['GPG_KEY_ID'],
                             current_app.config['GPG_PASSPHRASE_FILE'])
        return send_file(
            out,
            'application/zip',
            as_attachment=True,
            attachment_filename=fname + '.zip',
            add_etags=False)


class DeleteReportView(BaseView):
    template = 'forms/deletion_form.html'
    metadata_template = 'data/metadata/report_metadata.html'

    def rename_forecast(self, forecast):
        """Applies a percentile label to the end of a probabilistic forecast
        constant value name.
        """
        name = forecast['name']
        if 'constant_value' in forecast:
            constant_value = forecast['constant_value']
            if forecast['axis'] == 'x':
                units = api_varname_to_units(forecast['variable'])
                return f'{name} Prob(x <= {constant_value} {units}'
            else:
                return f'{name} Prob(f <= x) = {constant_value}%'
        else:
            return name

    def _object_pair_template_attributes(self, pair):
        """Load metadata for objects included in forecast/obs pairs.

        Parameters
        ----------
        pair:
            Dict created from an object in the `object_pairs` field of the
            Solar Forecast Arbiter API report JSON response.

        Returns
        -------
        dict:
            Dict containing the following keys and values:
            * forecast: dict of forecast metadata or None
            * observation: dict of observation metadata or None
            * aggregate: dict of aggregate metadata or None
            * reference_forecast: dict of forecast metadata or None
            * uncertainty: dependent on value
              * float: float
              * 'observation_uncertainty': The value of the observation's
                  uncertainty field if available.
              * None: None
            * cost: cost value of the pair (str or None)
            * forecast_view: The name of the forecast view relative to the
                data_dashboard blueprint e.g. accessible via
                `data_dashboard.<forecast_view>`.
        """
        forecast_type = pair['forecast_type']

        if forecast_type == 'forecast' or forecast_type == 'event_forecast':
            forecast_get = forecasts.get_metadata
            forecast_view = 'forecast_view'

        elif forecast_type == 'probabilistic_forecast':
            forecast_get = cdf_forecast_groups.get_metadata
            forecast_view = 'cdf_forecast_group_view'

        else:
            forecast_get = cdf_forecasts.get_metadata
            forecast_view = 'cdf_forecast_view'

        try:
            forecast_metadata = forecast_get(pair['forecast'])
        except DataRequestException:
            forecast_metadata = None
        else:
            forecast_metadata['name'] = self.rename_forecast(forecast_metadata)

        if pair.get('reference_forecast') is not None:
            try:
                reference_metadata = forecast_get(pair['reference_forecast'])
            except DataRequestException:
                reference_metadata = None
            else:
                reference_metadata['name'] = self.rename_forecast(
                    reference_metadata)
        else:
            reference_metadata = None

        if pair.get('observation') is not None:
            try:
                observation_metadata = observations.get_metadata(
                    pair['observation'])
            except DataRequestException:
                observation_metadata = None
        else:
            observation_metadata = None

        if pair.get('aggregate') is not None:
            try:
                aggregate_metadata = aggregates.get_metadata(
                    pair['aggregate'])
            except DataRequestException:
                aggregate_metadata = None
        else:
            aggregate_metadata = None

        if pair['uncertainty'] == 'observation_uncertainty':
            if observation_metadata is not None:
                uncertainty = observation_metadata['uncertainty']
            else:
                uncertainty = None
        else:
            uncertainty = pair.get('uncertainty')
        return {
            'forecast': forecast_metadata,
            'observation': observation_metadata,
            'aggregate': aggregate_metadata,
            'reference_forecast': reference_metadata,
            'uncertainty': uncertainty,
            'cost': pair.get('cost'),
            'forecast_view': forecast_view,
        }

    def load_pair_template_args(self):
        params = self.metadata['report_parameters']
        object_pairs = params['object_pairs']
        pair_template_args = []
        for pair in object_pairs:
            pair_args = self._object_pair_template_attributes(pair)
            # check if the user has access to some metadata before including
            # the object pair.
            if (
                pair_args['forecast'] is None
                and pair_args['observation'] is None
                and pair_args['aggregate'] is None
                and pair_args['reference_forecast'] is None
            ):
                continue
            pair_template_args.append(
                pair_args
            )
        return pair_template_args

    def set_template_args(self):
        object_pair_template_args = self.load_pair_template_args()
        self.template_args = {
            'data_type': 'report',
            'uuid': self.metadata['report_id'],
            'metadata': {
                'report_parameters': self.metadata['report_parameters']},
            'metadata_block': render_template(
                self.metadata_template,
                data_type='Report',
                metadata=self.metadata,
                object_pairs=object_pair_template_args,
            ),
        }

    def get(self, uuid):
        try:
            self.metadata = reports.get_metadata(uuid)
        except DataRequestException as e:
            return render_template(self.template, data_type='report',
                                   uuid=uuid, errors=e.errors)
        return super().get()

    def post(self, uuid):
        confirmation_url = url_for(
            'data_dashboard.delete_report',
            _external=True,
            uuid=uuid
        )
        if request.headers['Referer'] != confirmation_url:
            # If the user was directed from anywhere other than
            # the confirmation page, redirect to confirm.
            return redirect(confirmation_url)
        try:
            reports.delete(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
            return redirect(url_for('data_dashboard.delete_report',
                                    uuid=uuid))
        flash("Report deleted successfully")
        return redirect(url_for('data_dashboard.reports'))


class RecomputeReportView(BaseView):
    """View to recompute a report. Requests a recompute and redirects the user
    to the reports listing view.
    """
    def get(self, uuid):
        try:
            reports.recompute(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
        else:
            flash('Scheduled report recompute successfully. Wait 30 seconds '
                  'and refresh the page to view recomputed report.',
                  'message')
        return redirect(url_for('data_dashboard.report_view',
                                uuid=uuid))


class ReportCloneView(ReportForm):
    def __init__(self):
        # skip ReportForm init process to determine the applicable form based
        # on metadata
        pass

    def set_report_type(self):
        """Set the `report_type` instance variable based on the forecast types
        included in its `object_pairs`. Defaults to 'deterministic'.
        """
        object_pairs = self.metadata['report_parameters']['object_pairs']
        forecast_types = [pair['forecast_type'] for pair in object_pairs]
        if 'event_forecast' in forecast_types:
            self.report_type = 'event'
        elif ('probabilistic_forecast' in forecast_types
              or 'probabilistic_forecast_constant_value' in forecast_types):
            self.report_type = 'probabilistic'
        else:
            self.report_type = 'deterministic'

    def set_template_args(self):
        super().set_template_args()
        form_data = self.converter.payload_to_formdata(self.metadata)
        self.template_args.update({
            'form_data': form_data,
            'report_type': self.report_type,
        })

    def get(self, uuid):
        try:
            self.metadata = reports.get_metadata(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
            return redirect(url_for('data_dashboard.report_view',
                                    uuid=uuid))

        else:
            self.set_report_type()
            self.set_template()
            self.set_template_args()
            return render_template(self.template, **self.template_args)


class ReportOutageView(BaseView):
    """View that lists report outages for a specific report.
    """
    template = "data/report_outages.html"

    def set_template_args(self, uuid=None):
        self.template_args = {}
        try:
            report = reports.get_metadata(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
        else:
            self.template_args['page_title'] = "Report Outages"
            outages = report['outages']
            system_outages = list(filter(
                lambda x: x['report_id'] is None,
                outages
            ))
            report_outages = list(filter(
                lambda x: x['report_id'] is not None,
                outages
            ))
            self.template_args['system_outages'] = system_outages
            self.template_args['report_outages'] = report_outages
            self.template_args['metadata'] = report


class ReportOutageForm(BaseView):
    """Form for creating report outage."""
    template = "forms/report_outage_form.html"

    def set_template_args(self, uuid):
        self.template_args = {}
        self.template_args['page_title'] = "Add Report Outage"
        try:
            report = reports.get_metadata(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
        else:
            self.template_args['metadata'] = report

    def get(self, uuid=None):
        self.set_template_args(uuid)
        return render_template(self.template, **self.template_args)

    def post(self, uuid=None):
        form_data = request.form
        converter = converters.ReportOutageConverter
        formatted = converter.formdata_to_payload(form_data)
        try:
            reports.post_outage(uuid, formatted)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
            self.set_template_args(uuid)
            return render_template(
                self.template,
                form_data=form_data,
                **self.template_args
            )
        else:
            return redirect(url_for(
                "data_dashboard.report_outage_view",
                uuid=uuid
            ))


class ReportOutageDeletionForm(BaseView):
    """Form for deleting a single report outage.
    """
    template = "forms/report_outage_deletion_form.html"

    def set_template_args(self, uuid, outage_id):
        self.template_args = {}
        try:
            report = reports.get_metadata(uuid)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
        else:
            outage = None
            for report_outage in report['outages']:
                if report_outage['outage_id'] == outage_id:
                    outage = report_outage
                    break
            if outage is None:
                self.flash_api_errors({
                    "404": [
                        "The requested object could not be found. "
                        "You may need to request access from the "
                        "data owner."
                    ],
                })
            else:
                self.template_args['metadata'] = report
                self.template_args['outage'] = outage

    def get(self, uuid=None, outage_id=None):
        self.set_template_args(uuid, outage_id)
        return render_template(self.template, **self.template_args)

    def post(self, uuid=None, outage_id=None):
        try:
            reports.delete_outage(uuid, outage_id)
        except DataRequestException as e:
            self.flash_api_errors(e.errors)
            self.set_template_args(uuid)
            return render_template(
                self.template,
                **self.template_args
            )
        else:
            flash("Deleted outage successfully.")
            return redirect(url_for(
                "data_dashboard.report_outage_view",
                uuid=uuid
            ))

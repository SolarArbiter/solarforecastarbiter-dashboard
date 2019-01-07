from flask import Blueprint, render_template, abort
from sfa_dash.api_interface import demo_data
from sfa_dash.blueprints.base import BaseView

demo_blp = Blueprint('demo', 'demo', url_prefix='/demo')

class DemoViews(BaseView):
    def get(self, form_type):
        temp_args = {}
        if form_type=="site":
            return render_template('forms/demo_site_form.html')
        if form_type=="observation":
            metadata = demo_data.site
            temp_args['metadata'] = render_template('data/metadata/site_metadata.html', **metadata)
            return render_template('forms/demo_obs_form.html', **temp_args)
        if form_type=="forecast":
            return render_template('forms/demo_fx_form.html')
        if form_type=="upload":
            metadata = {'name': 'Ashland OR, ghi',
                        'variable': 'GHI (W/m^2)',
                        'obs_id': '123e4567-e89b-12d3-a456-426655440000',
                        'site_id': '123e4567-e89b-12d3-a456-426655440001',
                        'value_type': 'interval mean',
                        'interval_label': 'end'}
            temp_args['metadata'] = render_template('data/metadata/observation_metadata.html', **metadata)
            return render_template('forms/demo_obs_data_form.html', **temp_args)
        abort(404) 


demo_blp.add_url_rule('/<form_type>/', view_func=DemoViews.as_view('site_form'))



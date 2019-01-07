import pdb
from flask import Blueprint, jsonify, render_template, request, flash
from flask.views import MethodView
from sfa_dash.api_interface.requests import api_get, api_post
import time
import json
import requests


class CreateResourceForm(MethodView):
    type_map = {
        'string': 'text',
        'number': 'number',
    }
    def request_schema(self):
        r = requests.get('http://localhost:8080/schema/site')
        return json.loads(r.text)


    def get(self):
        json_dict = self.request_schema()
        form_fields = {}
        for key, value in json_dict[0]['definitions']['SiteSchema']['properties'].items():
            form_fields[key] = {
                'type': self.type_map.get(value['type'], None),
                'label': value.get('title', key),
                'name': key,
                'description': value.get('description', None ),
                'required': key in json_dict[0]['definitions']['SiteSchema']['required'],
            }
        form = render_template('forms/create_form.html', form_fields=form_fields)
        return form


    def post(self):
        form_data = request.form.copy()
        #TODO: post data to api, get errors/success & respond
        post_response = api_post('/sites/', form_data)
        return jsonify({'form data': form_data})

forms_blp = Blueprint('resource_form', 'resource_form', url_prefix="/create/")
forms_blp.add_url_rule('/site', view_func=CreateResourceForm.as_view('site'))

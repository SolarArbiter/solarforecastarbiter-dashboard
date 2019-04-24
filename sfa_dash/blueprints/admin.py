import json

from flask import (Blueprint, render_template, request, jsonify,
                   abort, redirect, url_for, make_response)
import pandas as pd
from sfa_dash.api_interface import (sites, observations, forecasts,
                                    cdf_forecast_groups)
from sfa_dash.blueprints.base import BaseView


class AdminView(BaseView):
    subnav_format = {
        '{users_url}': 'Users',
        '{roles_url}': 'Roles',
        '{permissions_url}': 'Permissions',
    }


    def template_args(self):
        subnav_kwargs = {
            'users_url': url_for('admin.users'),
            'roles_url':url_for('admin.roles'),
            'permissions_url':url_for('admin.permissions'),
        }
        return {'subnav': self.format_subnav(**subnav_kwargs)}

    def get(self):
        return render_template('forms/admin/admin.html',
                               **self.template_args())


class PermissionsListing(AdminView):
    def get(self):
        return render_template('forms/admin/permissions.html',
                               **self.template_args())


class RoleListing(AdminView):
    def get(self):
        return render_template('forms/admin/roles.html',
                               **self.template_args())


class UserListing(AdminView):
    def get(self):
        return render_template('forms/admin/users.html',
                               **self.template_args())


class PermissionsCreation(AdminView):
    allowed_data_types =['site', 'observation',
                         'forecast', 'cdf_forecast_group']
    def __init__(self, data_type):
        if data_type not in self.allowed_data_types:
            raise ValueError('invalid data_type')
        else:
            if data_type == 'observation':
                self.api_handle = observations
            elif data_type == 'forecast':
                self.api_handle = forecasts
            elif data_type == 'site':
                self.api_handle = sites
            elif data_type == 'cdf_forecast_group':
                self.api_handle = cdf_forecast_groups
            self.data_type = data_type

    def get(self):
        list_request = self.api_handle.list_metadata()
        table_data = list_request.json()
        return render_template("forms/admin/permissions_form.html",
                               table_data=table_data,
                               data_type=self.data_type,
                               **self.template_args())

    def post(self):
        request.form
        return jsonify(request.form)


admin_blp = Blueprint('admin', 'admin', url_prefix='/admin')
admin_blp.add_url_rule('/',
                       view_func=AdminView.as_view(
                            'admin')
                       )
                    
admin_blp.add_url_rule('/permissions/',
                       view_func=PermissionsListing.as_view(
                            'permissions')    
                       )
for data_type in PermissionsCreation.allowed_data_types:
    admin_blp.add_url_rule(f'/permissions/create/{data_type}',
                           view_func=PermissionsCreation.as_view(
                               f'{data_type}_permission',
                               data_type=data_type)
                           )
admin_blp.add_url_rule('/roles/',
                       view_func=RoleListing.as_view('roles'))
admin_blp.add_url_rule('/users/',
                       view_func=UserListing.as_view('users'))

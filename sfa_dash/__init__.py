from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import os  # NOQA


from flask import (
    Flask, redirect, url_for, render_template,
    session, request, send_from_directory,
    g
)  # NOQA
from flask_seasurf import SeaSurf  # NOQA
import sentry_sdk  # NOQA
from sentry_sdk.integrations.flask import FlaskIntegration  # NOQA


from sfa_dash.blueprints.auth0 import (make_auth0_blueprint,  # NOQA
                                       oauth_request_session)  # NOQA
from sfa_dash.api_interface import users  # NOQA
from sfa_dash.database import db, session_storage  # NOQA
from sfa_dash.errors import DataRequestException  # NOQA
from sfa_dash.filters import register_jinja_filters  # NOQA
from sfa_dash.template_globals import template_variables  # NOQA
from sfa_dash import error_handlers  # NOQA


def create_app(config=None):
    sentry_sdk.init(send_default_pii=False,
                    release=f'sfa-dash@{__version__}',
                    integrations=[FlaskIntegration()])

    app = Flask(__name__)
    config = config or 'sfa_dash.config.DevConfig'
    app.config.from_object(config)
    app.secret_key = app.config['SECRET_KEY']
    SeaSurf(app)
    register_jinja_filters(app)
    error_handlers.register_handlers(app)

    if app.config['SQLALCHEMY_DATABASE_URI']:
        db.init_app(app)
        db.create_all(app=app)

    make_auth0_blueprint(
        app,
        base_url=app.config['AUTH0_OAUTH_BASE_URL'],
        storage=session_storage)

    def protect_endpoint():
        try:
            authorized = oauth_request_session.authorized
        except ValueError:
            # no token set for user/no user set
            authorized = False

        # authorized == True means we have a token, not necessarily that it
        # hasn't expired, but refreshing is handled
        # by request_oauthlib and oauthlib
        # and the api validates expiration
        if not authorized:
            session['redirect_path'] = request.path
            return redirect(url_for('auth0.login'))

    @app.route('/')
    def index():
        # move index to app so all blueprints are secured
        # should probably test if authorized and show one
        # page, show a different page w/ login link otherwise
        return render_template('index.html')

    @app.route('/documentation/')
    def documentation():
        return render_template('documentation.html')

    @app.route('/changelog/')
    def changelog():
        return render_template('changelog.html')

    @app.route('/robots.txt')
    def robots():
        return send_from_directory('static', 'robots.txt')

    @app.context_processor
    def inject_globals():
        # Injects variables into all rendered templates
        global_template_args = {}
        current_user = session.get('userinfo')
        global_template_args['current_user'] = current_user
        if current_user is not None:
            if 'uuid' in request.view_args:
                uuid = request.view_args.get('uuid')
                try:
                    g.allowed_actions = users.actions_on(uuid)['actions']
                except DataRequestException:
                    # Allow for special cases to later set g.allowed_actions
                    # e.g. cdf_forecast_single, where permissions are dependent
                    # on the parent cdf_forecast_group
                    pass
            try:
                g.can_create = users.get_create_permissions()['can_create']
            except (DataRequestException):
                pass
        global_template_args.update(template_variables())
        return global_template_args

    @app.errorhandler(500)
    def server_error_handler(error):
        return render_template(
            "500.html",
            sentry_event_id=sentry_sdk.last_event_id(),
            dsn=os.getenv('SENTRY_DSN', '')), 500

    from sfa_dash.blueprints.main import data_dash_blp
    from sfa_dash.blueprints.form import forms_blp
    from sfa_dash.blueprints.admin import admin_blp

    for blp in (data_dash_blp, forms_blp, admin_blp):
        blp.before_request(protect_endpoint)
        app.register_blueprint(blp)
    return app


def create_app_with_metrics(config='sfa_dash.config.ProdConfig'):  # pragma: no cover  # NOQA
    from prometheus_flask_exporter.multiprocess import (
        GunicornPrometheusMetrics)
    app = create_app(config)
    GunicornPrometheusMetrics(app=app, group_by='url_rule')
    return app


def __getattr__(name):  # pragma: no cover
    if name == 'app':
        return create_app_with_metrics('sfa_dash.config.ProdConfig')
    elif name == 'dev_app':
        return create_app_with_metrics('sfa_dash.config.DevConfig')
    elif name == 'local_app':
        return create_app('sfa_dash.config.LocalConfig')
    else:
        raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


if __name__ == '__main__':
    app = create_app()
    app.run()

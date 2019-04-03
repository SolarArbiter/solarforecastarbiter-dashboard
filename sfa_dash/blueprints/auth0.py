from functools import partial


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask import url_for, redirect, current_app, session
from flask.globals import LocalProxy, _lookup_app_object
from flask_dance.consumer import OAuth2ConsumerBlueprint
from six.moves.urllib.parse import urlencode


auth0 = LocalProxy(partial(_lookup_app_object, 'auth0_oauth'))


def logout():
    session.clear()
    params = {'returnTo': url_for('data_dashboard.root_redirect',
                                  _external=True),
              'client_id': current_app.config['AUTH0_OAUTH_CLIENT_ID']}
    return redirect(
        current_app.config['AUTH0_OAUTH_BASE_URL'] + '/v2/logout?'
        + urlencode(params))


def make_auth0_blueprint(
        base_url, client_id=None, client_secret=None,
        scope=None, redirect_url=None,
        redirect_to=None, login_url=None,
        session_class=None,
        storage=None):
    scope = scope or ['openid', 'email', 'profile', 'offline_access']
    auth0_bp = OAuth2ConsumerBlueprint(
        'auth0', __name__,
        client_id=client_id,
        client_secret=client_secret,
        base_url=base_url,
        token_url=f'{base_url}/oauth/token',
        authorization_url=f'{base_url}/authorize',
        authorization_url_params={
            'audience': 'https://api.solarforecastarbiter.org'},
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        scope=scope,
        login_url=login_url,
        session_class=session_class,
        storage=storage,
        )
    auth0_bp.from_config['client_id'] = 'AUTH0_OAUTH_CLIENT_ID'
    auth0_bp.from_config['client_secret'] = 'AUTH0_OAUTH_CLIENT_SECRET'

    @auth0_bp.before_app_request
    def set_applocal_session():
        ctx = stack.top
        ctx.auth0_oauth = auth0_bp.session

    return auth0_bp

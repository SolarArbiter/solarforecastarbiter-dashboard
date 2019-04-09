from flask import redirect, url_for


from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError


def no_refresh_token(error):
    return redirect(url_for('auth0.login'))


def register_error_handlers(app):
    # This may be a temporary solution to tokens that do not auto-refresh
    app.register_error_handler(InvalidClientIdError, no_refresh_token)

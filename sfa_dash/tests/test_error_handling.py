def test_token_refresh_error(app):
    with app.test_client() as webapp:
        req = webapp.get('/observations/', follow_redirects=False)
    assert req.status_code == 302
    assert req.headers['Location'] == 'http://localhost/login/auth0'


def test_token_refresh_error_handler_called(app, mocker):
    handler = mocker.patch('sfa_dash.error_handlers.no_refresh_token')
    with app.test_client() as webapp:
        get = webapp.get('/observations/', base_url='http://localhost',
                         follow_redirects=False)
    assert get.status_code == 302
    assert get.headers['Location'] == 'http://localhost/login/auth0'
    handler.assert_called

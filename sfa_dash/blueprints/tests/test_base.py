import pytest


from sfa_dash.blueprints.base import BaseView


@pytest.mark.parametrize('errors,expected', [
    ({'it': ['broke']}, '(it) broke'),
    ({'2': ['er', 'rors']}, '(2) er, rors'),
])
def test_flash_errors_formatting(mocker, app, errors, expected):
    flasher = mocker.patch('sfa_dash.blueprints.base.flash')
    with app.test_request_context():
        BaseView().flash_api_errors(errors)
    flasher.assert_called_with(expected, 'error')

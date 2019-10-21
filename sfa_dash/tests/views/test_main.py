import pytest


from bs4 import BeautifulSoup as bs
from flask import url_for
from sfa_dash.conftest import BASE_URL


def test_no_arg_views(app, no_arg_route):
    with app.test_client() as dash:
        resp = dash.get(no_arg_route, base_url=BASE_URL)
        assert resp.status_code == 200
        page = bs(resp.data)
        assert page.table == ''

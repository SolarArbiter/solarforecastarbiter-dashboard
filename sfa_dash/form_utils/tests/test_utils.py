import pytest


from sfa_dash.form_utils import utils


def test_flatten_dict():
    original_dict = {
        'a': 1,
        'b': {'z': 5,
              'y': 4,
              'x': 3},
        'c': [1, 2, 3, 4]
    }
    expected_out = {
        'a': 1,
        'z': 5,
        'y': 4,
        'x': 3,
        'c': [1, 2, 3, 4],
    }
    out = utils.flatten_dict(original_dict)
    assert out == expected_out


@pytest.mark.parametrize('data,root,expected', [
    ({'time_hours': 10, 'time_minutes': 23}, 'time', '10:23'),
    ({'issue_time_hours': 5, 'issue_time_minutes': 2}, 'issue_time', '05:02'),
])
def test_parse_hhmm_field_from_form(data, root, expected):
    assert utils.parse_hhmm_field_from_form(data, root) == expected


@pytest.mark.parametrize('expected,root,data', [
    ({'time_hours': 10, 'time_minutes': 23},
     'time', {'time': '10:23'}),
    ({'issue_time_hours': 5, 'issue_time_minutes': 2},
     'issue_time', {'issue_time': '05:02'}),
])
def test_parse_hhmm_field_from_api(data, root, expected):
    assert utils.parse_hhmm_field_from_api(data, root) == expected


@pytest.mark.parametrize('data,root,expected', [
    ({'lead_time_number': 360,
      'lead_time_units': 'minutes'}, 'lead_time', 360),
    ({'lead_time_number': 3,
      'lead_time_units': 'hours'}, 'lead_time', 180),
    ({'lead_time_number': 2,
      'lead_time_units': 'days'}, 'lead_time', 2880),
])
def test_parse_timedelta_from_form(data, root, expected):
    assert utils.parse_timedelta_from_form(data, root) == expected


@pytest.mark.parametrize('expected,root,data', [
    ({'lead_time_number': 90,
      'lead_time_units': 'minutes'}, 'lead_time', {'lead_time': 90}),
    ({'lead_time_number': 3,
      'lead_time_units': 'hours'}, 'lead_time', {'lead_time': 180}),
    ({'lead_time_number': 2,
      'lead_time_units': 'days'}, 'lead_time', {'lead_time': 2880}),
])
def test_parse_timedelta_from_api(data, root, expected):
    assert utils.parse_timedelta_from_api(data, root) == expected


@pytest.mark.parametrize('from_dict', [
    {'aggregate_id': 'someaggregateid'},
    {'site_id': 'somesiteid'},
    {'aggregate_id': 'someaggregateid', 'site_id': None},
    {'aggregate_id': None, 'site_id': 'somesiteid'},
])
def test_set_location_id(from_dict):
    response_dict = {}
    utils.set_location_id(from_dict, response_dict)
    for key in list(from_dict.keys()):
        assert from_dict[key] == response_dict[key]


def test_set_location_id_no_location_key():
    original_dict = {'key': 'not_to_mangle'}
    response_dict = original_dict.copy()
    utils.set_location_id({}, response_dict)
    assert original_dict == response_dict

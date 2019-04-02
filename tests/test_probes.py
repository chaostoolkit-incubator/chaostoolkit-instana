from unittest.mock import patch

from chaoslib.exceptions import ActivityFailed
from chaosinstana.probes import get_all_events_in_window
from chaosinstana.probes import convert_time

from tests.fixtures import config, responses, secrets


@patch('chaosinstana.probes.get_all_events', autospec=True)
def test_get_all_events_in_window(get_all_events):
    get_all_events.return_value = responses.FakeResponse(
        status_code=200,
        text=None,
        json=lambda: responses.events)

    result = get_all_events_in_window(
        "", "", config.config, secrets.secrets)
    assert result.json() == responses.events


def test_check_milli_since_epoch():
    orig_milli_since_epoch = "1554709383790"
    expected_result = 1554709383790
    result_milli_since_epoch = convert_time(
        orig_milli_since_epoch)
    assert isinstance(result_milli_since_epoch, int)
    assert result_milli_since_epoch == expected_result


def test_check_5_minutes_ago():
    time_str = "5 minutes ago"
    result_milli_since_epoch = convert_time(time_str)
    assert isinstance(result_milli_since_epoch, int)


def test_check_date_string():
    time_str = "08 April 2019 08:30"
    result_milli_since_epoch = convert_time(time_str)
    print(result_milli_since_epoch)
    assert isinstance(result_milli_since_epoch, int)


def test_check_date_string_invalid_date():
    time_str = "invalid date str"
    try:
        result_milli_since_epoch = convert_time(
                                    time_str)
        print(result_milli_since_epoch)
    except ActivityFailed as error:
        assert str(error) == "Invalid date string provided"

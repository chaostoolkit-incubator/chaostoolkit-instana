from unittest.mock import patch

from chaoslib.exceptions import ActivityFailed
import requests_mock

from chaosinstana.probes import get_all_events_in_window
from chaosinstana.probes import convert_time
from chaosinstana.probes import has_severity
from chaosinstana.types import Events

from tests.fixtures import config, responses, secrets


@patch('chaosinstana.probes.get_all_events', autospec=True)
def test_get_all_events_in_window(get_all_events):
    get_all_events.return_value = responses.FakeResponse(
        status_code=200,
        text=None,
        json=lambda: responses.events)

    result = get_all_events_in_window(from_time="", to_time="",
                                      configuration=config.config,
                                      secrets=secrets.secrets)
    assert result.json() == responses.events


def test_has_severity_level(sample_events: Events):
    result = has_severity(sample_events, 10)
    assert result


def test_does_not_have_severity_level(sample_events: Events):
    result = has_severity(sample_events, 2)
    assert result is False


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


def test_empty_date_string():
    time_str = ""
    result_milli_since_epoch = convert_time(time_str)
    assert result_milli_since_epoch is None


def test_none_date_string():
    time_str = None
    result_milli_since_epoch = convert_time(time_str)
    assert result_milli_since_epoch is None


def test_check_date_string_invalid_date():
    time_str = "invalid date str"
    try:
        convert_time(time_str)
    except ActivityFailed as error:
        assert str(error) == "Invalid date string provided"


def testapi():
    c = {
        "instana_host": "https://testinstanna.io"
    }
    s = {
        "instana_api_token": "1234456"
    }
    with requests_mock.Mocker() as m:
        m.get("https://testinstanna.io/api/events?from=155566&to=1555667",
              json={
                "events": "event"
              })
        data = get_all_events_in_window(
            from_time="155566",
            to_time="1555667",
            configuration=c,
            secrets=s)
        assert data == {"events": "event"}

import dateparser

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from .api import get_all_events

__all__ = ["get_all_events_in_window", "convert_time"]


def convert_time(source_time: str) -> int:
    """
    If the `source_time` is an int, just use it as is, otherwise parse the
    string using dateparser.parse, this should help with datestrings in
    other langauges and also supports relative dates
    for further info see https://pypi.org/project/dateparser/
    """
    try:
        return int(source_time)
    except ValueError:
        # source_time_string not an int
        start_dt = dateparser.parse(source_time)
        if not start_dt:
            logger.error("Invalid date string provided")
            raise ActivityFailed("Invalid date string provided")
        return int(start_dt.timestamp() * 1000)


def get_all_events_in_window(from_time: str = None, to_time: str = None,
                             configuration: Configuration = None,
                             secrets: Secrets = None) -> str:
    """
    get all events from instana within a time window, given by the from_time
    and the to_time
    """

    if from_time:
        from_time = convert_time(from_time)

    if to_time:
        to_time = convert_time(to_time)

    res = get_all_events(
        from_time, to_time, configuration, secrets)
    return res
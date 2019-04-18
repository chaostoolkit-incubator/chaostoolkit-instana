import dateparser
# import datetime
import time


from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from .api import get_all_events

__all__ = ["get_all_events_in_window", "has_critical_events_in_window",
           "has_warning_events_in_window", "has_change_events_in_window"]

CRITICAL_LEVEL = 10
WARNING_LEVEL = 5
CHANGE_LEVEL = -1


def has_critical_events_in_window(from_time: str = None, to_time: str = None,
                                  delay: int = 0,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> str:
    """
    returns a boolean indicating if there have been any critical events in a
    time window
    """
    event_data = get_all_events_in_window(from_time=from_time,
                                          to_time=to_time,
                                          delay=delay,
                                          configuration=configuration,
                                          secrets=secrets)
    return has_severity(event_data=event_data, severity_level=CRITICAL_LEVEL)


def has_warning_events_in_window(from_time: str = None, to_time: str = None,
                                 delay: int = 0,
                                 configuration: Configuration = None,
                                 secrets: Secrets = None) -> str:
    """
    returns a boolean indicating if there have been any warning events in a
    time window
    """
    event_data = get_all_events_in_window(from_time=from_time, to_time=to_time,
                                          delay=delay,
                                          configuration=configuration,
                                          secrets=secrets)
    return has_severity(event_data=event_data, severity_level=WARNING_LEVEL)


def has_change_events_in_window(from_time: str = None, to_time: str = None,
                                delay: int = 0,
                                configuration: Configuration = None,
                                secrets: Secrets = None) -> str:
    """
    returns a boolean indicating if there have been any change events in a
    time window
    """
    event_data = get_all_events_in_window(from_time=from_time, to_time=to_time,
                                          delay=delay,
                                          configuration=configuration,
                                          secrets=secrets)
    return has_severity(event_data=event_data, severity_level=CHANGE_LEVEL)


def get_all_events_in_window(from_time: str = None, to_time: str = None,
                             delay: int = 0,
                             configuration: Configuration = None,
                             secrets: Secrets = None) -> str:
    """
    get all events from instana within a time window, given by the from_time
    and the to_time
    """
    logger.info("Instana probe delay is: {} seconds.".format(delay))
    time.sleep(delay)
    from_milli = convert_time(from_time)
    to_milli = convert_time(to_time)
    # fr_date = datetime.datetime.fromtimestamp(int(from_milli)/1000.0)
    # to_date = datetime.datetime.fromtimestamp(to_milli/1000.0)

    # logger.debug("from_time {} ({})".format(from_milli, fr_date))
    # logger.debug("to_time {} ({})".format(to_milli, to_date))

    res = get_all_events(
        from_milli, to_milli, configuration, secrets)
    return res


###############################################################################
# Internals
###############################################################################
def convert_time(source_time: str) -> int:
    """
    If the `source_time` is an int, just use it as is, otherwise parse the
    string using dateparser.parse, this should help with datestrings in
    other langauges and also supports relative dates
    for further info see https://pypi.org/project/dateparser/
    """
    if not source_time:
        return

    try:
        return int(source_time)
    except ValueError:
        # source_time_string not an int
        start_dt = dateparser.parse(source_time)
        if not start_dt:
            logger.error("Invalid date string provided")
            raise ActivityFailed("Invalid date string provided")
        return int(start_dt.timestamp() * 1000)


def has_severity(event_data, severity_level):
    """
    Loops thorugh event data (expecting json array) and
    looks for a severity element, if that element equals the severity_level
    parameter given it returns True, if it reaches the end of the loop without
    finding the severity_level it returns False. Any expection also return
    false
    """
    try:
        for event in event_data:
            severity = event.get("severity")
            if severity == severity_level:
                logger.debug("has_severity for severity_level: {} is True"
                             .format(severity_level))
                return True

        logger.debug("has_severity for severity_level: {} is False"
                     .format(severity_level))
        return False
    except ValueError:
        logger.error("has_severity error parsing event_data")
        return False

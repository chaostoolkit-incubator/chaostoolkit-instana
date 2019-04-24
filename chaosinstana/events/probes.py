import dateparser
import datetime
import time

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosinstana.types import Events
from chaosinstana.api import get_all_events, get_event

__all__ = ["get_all_events_in_window", "has_change_events_in_window",
           "has_critical_events_in_window", "has_warning_events_in_window",
           "has_warning_or_critical_events_in_window"]

CRITICAL_LEVEL = 10
WARNING_LEVEL = 5
CHANGE_LEVEL = -1


def has_warning_or_critical_events_in_window(from_time: str = None, to_time:
                                             str = None,
                                             delay: int = 0,
                                             configuration: Configuration
                                             = None,
                                             secrets: Secrets = None) -> bool:
    """
    Returns a boolean indicating if there have been any critical or warning
    events in a time window
    """
    warning_events = has_warning_events_in_window(from_time=from_time,
                                                  to_time=to_time,
                                                  delay=delay,
                                                  configuration=configuration,
                                                  secrets=secrets)
    critical_events = has_critical_events_in_window(
                                                from_time=from_time,
                                                to_time=to_time,
                                                delay=delay,
                                                configuration=configuration,
                                                secrets=secrets)

    return critical_events | warning_events


def has_critical_events_in_window(from_time: str = None, to_time: str = None,
                                  delay: int = 0,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> bool:
    """
    Returns a boolean indicating if there have been any critical events in a
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
                                 secrets: Secrets = None) -> bool:
    """
    Returns a boolean indicating if there have been any warning events in a
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
    Returns a boolean indicating if there have been any change events in a
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
    Get all events from instana within a time window, given by the from_time
    and the to_time
    """
    logger.info("Instana probe delay is: {} seconds.".format(delay))
    time.sleep(delay)
    from_milli = convert_time(from_time)
    to_milli = convert_time(to_time)
    logger.debug("from_time {} ({})".
                 format(from_milli, milli_to_date_time(from_milli)))
    logger.debug("to_time {} ({})".
                 format(to_milli, milli_to_date_time(to_milli)))
    res = get_all_events(from_time=from_milli, to_time=to_milli,
                         configuration=configuration, secrets=secrets)

    return res


def get_event_content(event_id: str, delay: int = 0,
                      configuration: Configuration = None,
                      secrets: Secrets = None) -> str:
    """
    Get the event with the provided event id from instana, delay the request
    if required
    """
    logger.info("Instana probe delay is: {} seconds.".format(delay))
    time.sleep(delay)

    res = get_event(event_id=event_id, configuration=configuration,
                    secrets=secrets)
    return res


###############################################################################
# Internals
###############################################################################
def milli_to_date_time(milli: int) -> str:
    try:
        return datetime.datetime.fromtimestamp(milli/1000.0).strftime(
                                                         '%Y-%m-%d %H:%M:%S')
    except TypeError as e:
        logger.debug("TypeError in miili_to_date_time exception: {}".format(e))


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


def has_severity(event_data: Events, severity_level: int) -> bool:
    """
    Loops through event data (expecting json array) and
    looks for a severity element, if that element equals the severity_level
    parameter given it returns True, if it reaches the end of the loop without
    finding the severity_level it returns False. Any expection also return
    false
    """
    for event in event_data:
        severity = event.get("severity")
        if severity == severity_level:
            logger.debug("has_severity for severity_level: {} is True"
                         .format(severity_level))
            return True

    logger.debug("has_severity for severity_level: {} is False"
                 .format(severity_level))
    return False

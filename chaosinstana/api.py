# -*- coding: utf-8 -*-
from typing import Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger
import requests

from chaosinstana.types import InstanaResponse


__all__ = ['get_all_events', 'get_event']


def execute_instana_get_request(url: str, params: Dict,
                                secrets: Secrets) -> InstanaResponse:
    """
     Call the instana rest api using the url amd params provided, use an
     Authorization header from the secrets provded
    """
    logger.debug("execute_instana_get_request")
    logger.debug("url is : {}".format(url))
    logger.debug("params : {}".format(params))
    r = requests.get(
        url=url,
        params=params,
        headers={
            "Authorization": "apiToken {}".format(
                secrets.get("instana_api_token"))
        }
    )
    if r.status_code > 399:
        raise ActivityFailed("failed to call '{u}': {c} => {s}".format(
            u=url, c=r.status_code, s=r.text))

    logger.debug("Instana response status code: {}".format(r.status_code))
    logger.debug("Instana json response: {}".format(r.json()))

    return r.json()


def get_all_events(from_time: str, to_time: str,
                   configuration: Configuration,
                   secrets: Secrets) -> InstanaResponse:
    """
     Get all events from instana within a time window, given by the from_time
     and the to_time for details of the api see
     https://instana.github.io/openapi/#tag/Events
    """
    logger.debug("get_all_events")
    instana_host = configuration.get("instana_host")
    instana_api_token = secrets.get("instana_api_token")

    if not (instana_host and instana_api_token):
        raise ActivityFailed(
            "No Instana Host or API Token Secrete were found.")

    url = "{}/api/events".format(
            configuration.get("instana_host"))

    params = {}
    if from_time:
        params["from"] = from_time

    if to_time:
        params["to"] = to_time

    result = execute_instana_get_request(url, params, secrets)
    return result


def get_event(event_id: str, configuration: Configuration,
              secrets: Secrets) -> InstanaResponse:
    """
     Get all an event from instana with the privded event_id for details of
     the api see https://instana.github.io/openapi/#operation/getEvent
    """
    logger.debug("get_event")
    instana_host = configuration.get("instana_host")
    instana_api_token = secrets.get("instana_api_token")

    if not (instana_host and instana_api_token):
        raise ActivityFailed(
            "No Instana Host or API Token Secrete were found.")

    url = "{}/api/events/{}".format(
            configuration.get("instana_host"), event_id)

    params = {}

    result = execute_instana_get_request(url, params, secrets)

    return result

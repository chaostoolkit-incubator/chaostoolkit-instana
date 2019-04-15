# -*- coding: utf-8 -*-
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger
import requests


__all__ = ['get_all_events']


def get_all_events(from_time: str, to_time: str,
                   configuration: Configuration, secrets: Secrets) -> str:
    """
     Get all events from instana within a time window, given by the from_time
     and the to_time for details of the api see
     https://instana.github.io/openapi/#tag/Events
    """
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

    logger.debug("url: {}".format(url))
    logger.debug("params: {}".format(params))

    r = requests.get(
        url=url,
        params=params,
        headers={
            "Authorization": "apiToken {}".format(
                secrets.get("instana_api_token"))
        }
    )
    logger.debug("r.json(): {}".format(r.json()))

    return r.json()

# -*- coding: utf-8 -*-
from typing import Any, Dict

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

    if (instana_host and instana_api_token):

        url = "{}/api/events".format(
            configuration.get("instana_host"))

        params = {}
        if (from_time):
            params["from"] = from_time

        if (to_time):
            params["to"] = to_time

        auth_header_key = "authorization"
        auth_header_contents = "apiToken " + secrets.get("instana_api_token")

        r = requests.get(url=url,
                         params=params,
                         headers={auth_header_key: auth_header_contents})

        data = r.json()

        return data
    else:
        logger.warning("No Instana Host or API Token Secrete were found.")

# -*- coding: utf-8 -*-
from typing import Any


class FakeResponse:
    def __init__(self, status_code: int = 200, text: str = None,
                 json: Any = None):
        self.status_code = status_code
        self.text = text
        self.json = json


events = [{
    'eventId': '_ymwBZ-sRmiNv1VlXMjK2A',
    'start': 1554186894000,
    'end': 1554186984000,
    'problem': 'Change detected',
    'fixSuggestion': 'The value **label** has changed from **\"Unknown\"** to **\"/app\\\\.jar \\\\-\\\\-spring\\\\.profiles\\\\.active=docker\"**.',
    'severity': -1,
    'snapshotId': 'jUtSJ9JOmG1rhrFATKSUCC53zJY'
}]

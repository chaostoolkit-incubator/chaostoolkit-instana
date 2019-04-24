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
    'fixSuggestion': 'any fix',
    'severity': -1,
    'snapshotId': 'jUtSJ9JOmG1rhrFATKSUCC53zJY'
}]


change_and_warning_events = [{
    'severity': -1
    },
    {
    'severity': 5
    }]

change_and_critical_events = [{
    'severity': -1
    },
    {
    'severity': 10
    }]

warning_and_critical_events = [{
    'severity': 5
    },
    {
    'severity': 10,
    }]

change_events = [{
    'severity': -1
}]

critical_events = [{
    'severity': 10
}]

warning_events = [{
    'severity': 5
}]

no_severity_events = [{
}]

invalid_severity_events = [{
    'severity': ""
}]

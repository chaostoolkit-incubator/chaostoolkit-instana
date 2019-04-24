import json
import os


import pytest
from chaosinstana.types import Events

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")


@pytest.fixture
def sample_file() -> str:
    return os.path.join(fixtures_dir, "sample_events.json")


@pytest.fixture
def sample_events(sample_file: str) -> Events:
    with open(sample_file, 'r') as fp:
        return json.load(fp)

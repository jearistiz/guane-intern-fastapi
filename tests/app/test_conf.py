from collections.abc import Mapping

from app import config


def test_sttgs():
    assert isinstance(config.sttgs, Mapping)

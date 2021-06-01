from app import VERSION


def test_version():
    assert len(VERSION.split('.')) == 3

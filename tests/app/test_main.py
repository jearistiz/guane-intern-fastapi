from fastapi import FastAPI

from app import main


def test_app():
    assert isinstance(main.app, FastAPI)

import pytest
from src.engine.runner import run


def test_full_pipeline():
    run()
    assert True
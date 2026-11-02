"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes.notes import _store


@pytest.fixture(autouse=True)
def reset_in_memory_store():
    """Clear in-memory notes store before and after each test."""
    _store._notes.clear()
    yield
    _store._notes.clear()


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)

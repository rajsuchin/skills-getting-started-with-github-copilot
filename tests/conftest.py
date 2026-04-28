import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test to ensure isolation."""
    original_participants = {
        name: list(data["participants"]) for name, data in activities.items()
    }
    yield
    for name, data in activities.items():
        data["participants"] = original_participants[name]


@pytest.fixture
def client():
    """Return a FastAPI TestClient for the app."""
    return TestClient(app)

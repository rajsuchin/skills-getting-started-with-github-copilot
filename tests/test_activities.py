"""
Integration tests for the Mergington High School API.

Covers:
- GET /activities
- POST /activities/{activity_name}/signup
- DELETE /activities/{activity_name}/participants/{email}
"""


def test_get_activities_returns_all(client):
    """GET /activities should return a dict of all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data


def test_get_activities_includes_expected_fields(client):
    """Each activity should have description, schedule, max_participants, and participants."""
    response = client.get("/activities")
    for activity in response.json().values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_successful(client):
    """A new student should be able to sign up for an existing activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    assert response.status_code == 200
    assert "newstudent@mergington.edu" in response.json()["message"]


def test_signup_duplicate_raises_400(client):
    """Signing up an already-enrolled student should return 400."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity_raises_404(client):
    """Signing up for an activity that does not exist should return 404."""
    response = client.post(
        "/activities/Underwater Basket Weaving/signup",
        params={"email": "anyone@mergington.edu"},
    )
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants/{email}
# ---------------------------------------------------------------------------

def test_delete_participant_successful(client):
    """An enrolled participant should be removable from an activity."""
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    assert response.status_code == 200
    assert "michael@mergington.edu" in response.json()["message"]


def test_delete_participant_not_found_raises_404(client):
    """Removing a participant not enrolled in the activity should return 404."""
    response = client.delete(
        "/activities/Chess Club/participants/ghost@mergington.edu"
    )
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()


def test_delete_participant_activity_not_found_raises_404(client):
    """Removing a participant from a non-existent activity should return 404."""
    response = client.delete(
        "/activities/Nonexistent Club/participants/anyone@mergington.edu"
    )
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()

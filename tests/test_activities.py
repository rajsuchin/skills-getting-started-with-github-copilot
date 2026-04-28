"""
Integration tests for the Mergington High School API.

Covers:
- GET /activities
- POST /activities/{activity_name}/signup
- DELETE /activities/{activity_name}/participants/{email}
"""


def test_get_activities_returns_all(client):
    """GET /activities should return a dict of all activities."""
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data


def test_get_activities_includes_expected_fields(client):
    """Each activity should have description, schedule, max_participants, and participants."""
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
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
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_signup_duplicate_raises_400(client):
    """Signing up an already-enrolled student should return 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity_raises_404(client):
    """Signing up for an activity that does not exist should return 404."""
    # Arrange
    activity_name = "Underwater Basket Weaving"
    email = "anyone@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants/{email}
# ---------------------------------------------------------------------------

def test_delete_participant_successful(client):
    """An enrolled participant should be removable from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_delete_participant_not_found_raises_404(client):
    """Removing a participant not enrolled in the activity should return 404."""
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()


def test_delete_participant_activity_not_found_raises_404(client):
    """Removing a participant from a non-existent activity should return 404."""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "anyone@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()

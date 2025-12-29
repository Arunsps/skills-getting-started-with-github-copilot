from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # ensure an expected activity exists
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Basketball Team"
    email = "pytest-user@example.com"

    # Ensure participant not present
    res = client.get("/activities")
    assert res.status_code == 200
    participants = res.json()[activity]["participants"]
    if email in participants:
        # cleanup if left over from previous runs
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json()["message"]

    # Participant present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email in participants

    # Remove participant
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert "Unregistered" in res.json()["message"]

    # Ensure removed
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email not in participants

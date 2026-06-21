from urllib.parse import quote


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.delete(
        f"/activities/{quote(activity)}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Unknown Club')}/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants",
        params={"email": "nobody@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_missing_email_returns_422(client):
    response = client.delete(f"/activities/{quote('Chess Club')}/participants")

    assert response.status_code == 422

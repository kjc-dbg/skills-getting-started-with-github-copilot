from urllib.parse import quote


def test_signup_adds_participant(client):
    email = "new-student@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        f"/activities/{quote('Unknown Club')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_email_returns_422(client):
    response = client.post(f"/activities/{quote('Chess Club')}/signup")

    assert response.status_code == 422

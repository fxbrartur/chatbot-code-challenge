from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# Test data
test_survey = {
    "survey_id": "test_survey",
    "title": "Test Survey",
    "questions": [
        {
            "id": 1,
            "question": "What is your favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        }
    ]
}

test_survey_update = {
    "title": "Updated Test Survey",
    "questions": [
        {
            "id": 1,
            "question": "What is your favorite framework?",
            "options": ["FastAPI", "Django", "Flask"]
        }
    ]
}

test_response_id = "response_1"


def test_get_all_survey_responses():
    """Test retrieving all survey responses."""
    response = client.get("/admin/survey_responses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_surveys():
    """Test retrieving all surveys."""
    response = client.get("/admin/surveys")
    assert response.status_code == 200

    surveys = response.json()
    assert len(surveys) == 3
    assert any(survey["id"] == "ice_cream_preferences" for survey in surveys)
    assert any(survey["id"] == "cake_preferences" for survey in surveys)
    assert any(survey["id"] == "beer_preferences" for survey in surveys)


def test_create_survey():
    """Test creating a new survey."""
    response = client.post("/admin/surveys", json=test_survey)
    assert response.status_code == 200
    assert response.json() == {"message": "Survey created successfully."}


def test_update_survey():
    """Test updating an existing survey."""
    # Create the survey first
    client.post("/admin/surveys", json=test_survey)

    # Update the survey
    response = client.put(f"/admin/surveys/{test_survey['survey_id']}", json=test_survey_update)
    assert response.status_code == 200
    assert response.json() == {"message": "Survey updated successfully."}


def test_delete_survey():
    """Test deleting an existing survey."""
    # Create the survey first
    client.post("/admin/surveys", json=test_survey)

    # Delete the survey
    response = client.delete(f"/admin/surveys/{test_survey['survey_id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Survey deleted successfully."}

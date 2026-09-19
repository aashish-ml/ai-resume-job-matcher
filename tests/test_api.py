from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "ai-resume-job-matcher"


# ---------------------------------------------------------
# Match Endpoint - Valid Request
# ---------------------------------------------------------

def test_match_endpoint():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "AI/ML Engineer\n"
            "Skills: Python, SQL, Machine Learning, "
            "Scikit-learn, FastAPI\n"
            "Projects: Built a customer churn prediction "
            "system using Python and Scikit-learn.\n"
            "Education: Bachelor of Arts"
        ),
        "job_description": (
            "AI/ML Engineer role requiring Python, SQL, "
            "Machine Learning, FastAPI, Docker and "
            "Scikit-learn skills."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resume_name"] == "Alex Sharma"

    assert "job_title" in data
    assert "match_percentage" in data
    assert "matched_skills" in data
    assert "missing_skills" in data
    assert "extra_skills" in data
    assert "skill_score" in data
    assert "skill_score_max" in data

    assert data["pipeline_status"] == "success"


# ---------------------------------------------------------
# Match Endpoint - Empty Resume
# ---------------------------------------------------------

def test_match_endpoint_empty_resume():
    payload = {
        "resume_text": "",
        "job_description": (
            "AI/ML Engineer requiring Python and SQL."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Match Endpoint - Empty Job Description
# ---------------------------------------------------------

def test_match_endpoint_empty_job_description():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "Skills: Python, SQL, Machine Learning."
        ),
        "job_description": "",
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Match Endpoint - Missing Resume Field
# ---------------------------------------------------------

def test_match_endpoint_missing_resume_text():
    payload = {
        "job_description": (
            "AI/ML Engineer requiring Python and SQL."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Match Endpoint - Missing Job Description
# ---------------------------------------------------------

def test_match_endpoint_missing_job_description():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "Skills: Python, SQL, Machine Learning."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Match Endpoint - Response Structure
# ---------------------------------------------------------

def test_match_response_structure():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "AI/ML Engineer\n"
            "Skills: Python, SQL, Machine Learning, "
            "Scikit-learn, FastAPI"
        ),
        "job_description": (
            "AI/ML Engineer requiring Python, SQL, "
            "Machine Learning, FastAPI, Docker and "
            "Scikit-learn skills."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    expected_keys = {
        "resume_name",
        "job_title",
        "match_percentage",
        "matched_skills",
        "missing_skills",
        "extra_skills",
        "matched_count",
        "missing_count",
        "extra_count",
        "skill_score",
        "skill_score_max",
        "pipeline_status",
    }

    assert expected_keys.issubset(data.keys())


# ---------------------------------------------------------
# Match Endpoint - Score Validation
# ---------------------------------------------------------

def test_match_score_validation():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "Skills: Python, SQL, Machine Learning, "
            "Scikit-learn, FastAPI"
        ),
        "job_description": (
            "AI/ML Engineer requiring Python, SQL, "
            "Machine Learning, FastAPI, Docker and "
            "Scikit-learn skills."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert 0 <= data["match_percentage"] <= 100
    assert 0 <= data["skill_score"] <= data["skill_score_max"]


# ---------------------------------------------------------
# Match Endpoint - Pipeline Status
# ---------------------------------------------------------

def test_match_pipeline_status():
    payload = {
        "resume_text": (
            "Alex Sharma\n"
            "Skills: Python, SQL, Machine Learning."
        ),
        "job_description": (
            "AI/ML Engineer requiring Python, SQL "
            "and Machine Learning."
        ),
    }

    response = client.post(
        "/match",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["pipeline_status"] == "success"

    # ============================================================
# Validation Error Tests
# ============================================================

def test_match_validation_error():
    """
    Verify that empty resume and job description
    are rejected by request validation.
    """

    response = client.post(
        "/match",
        json={
            "resume_text": "",
            "job_description": "",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["message"] == "Request validation failed."

    locations = [
        detail["loc"]
        for detail in data["details"]
    ]

    assert ["body", "resume_text"] in locations
    assert ["body", "job_description"] in locations

    # ============================================================
# Whitespace Validation Test
# ============================================================

def test_match_whitespace_validation_error():
    """
    Verify that whitespace-only resume and job description
    are rejected by request validation.
    """

    response = client.post(
        "/match",
        json={
            "resume_text": "   ",
            "job_description": "   ",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["message"] == "Request validation failed."

    locations = [
        detail["loc"]
        for detail in data["details"]
    ]

    assert ["body", "resume_text"] in locations
    assert ["body", "job_description"] in locations
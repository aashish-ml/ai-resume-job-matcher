from pathlib import Path

import pytest

from src.pipeline.matcher_pipeline import run_matching_pipeline


# ============================================================
# Test 1: End-to-End Pipeline
# ============================================================

def test_matching_pipeline_with_sample_resume():
    """
    Verify the complete resume-job matching pipeline.
    """

    resume_path = Path("data/raw/sample_resume.txt")

    job_description = (
        "AI/ML Engineer role requiring Python, SQL, "
        "Machine Learning, FastAPI, Docker and "
        "Scikit-learn skills."
    )

    result = run_matching_pipeline(
        str(resume_path),
        job_description,
    )

    assert isinstance(result, dict)

    assert result["pipeline_status"] == "success"

    assert result["resume_name"] == "Alex Sharma"

    assert "AI/ML Engineer" in result["job_title"]

    assert result["match_percentage"] == 83.33

    assert result["matched_count"] == 5

    assert result["missing_count"] == 1

    assert result["extra_count"] == 0

    assert result["skill_score"] == 83.33

    assert result["skill_score_max"] == 100.0

    assert "docker" in result["missing_skills"]


# ============================================================
# Test 2: Raw Resume Text Input
# ============================================================

def test_matching_pipeline_with_raw_resume_text():
    """
    Verify that the pipeline also accepts raw resume text
    instead of a file path.
    """

    resume_text = """
    Alex Sharma

    AI/ML Engineer

    Skills:
    Python, SQL, Machine Learning, FastAPI, Scikit-learn

    Education:
    Bachelor of Arts
    """

    job_description = (
        "AI/ML Engineer requiring Python, SQL, "
        "Machine Learning and FastAPI."
    )

    result = run_matching_pipeline(
        resume_text,
        job_description,
    )

    assert result["pipeline_status"] == "success"

    assert result["resume_name"] == "Alex Sharma"

    assert result["skill_score"] >= 0

    assert result["skill_score"] <= 100


# ============================================================
# Test 3: Empty Resume Input
# ============================================================

def test_matching_pipeline_rejects_empty_resume():
    """
    Verify that an empty resume is rejected.
    """

    job_description = (
        "AI/ML Engineer requiring Python and SQL."
    )

    with pytest.raises(ValueError):
        run_matching_pipeline(
            "",
            job_description,
        )


# ============================================================
# Test 4: Empty Job Description
# ============================================================

def test_matching_pipeline_rejects_empty_job_description():
    """
    Verify that an empty job description is rejected.
    """

    resume_text = """
    Alex Sharma

    Skills:
    Python, SQL, Machine Learning
    """

    with pytest.raises(ValueError):
        run_matching_pipeline(
            resume_text,
            "",
        )


# ============================================================
# Test 5: Invalid Resume Input Type
# ============================================================

def test_matching_pipeline_rejects_invalid_resume_type():
    """
    Verify that non-string resume input is rejected.
    """

    job_description = (
        "AI/ML Engineer requiring Python and SQL."
    )

    with pytest.raises(ValueError):
        run_matching_pipeline(
            123,
            job_description,
        )


# ============================================================
# Test 6: Invalid Job Description Type
# ============================================================

def test_matching_pipeline_rejects_invalid_job_type():
    """
    Verify that non-string job description input is rejected.
    """

    resume_text = """
    Alex Sharma

    Skills:
    Python, SQL, Machine Learning
    """

    with pytest.raises(ValueError):
        run_matching_pipeline(
            resume_text,
            123,
        )
"""
Pydantic schemas for the AI Resume Job Matcher API.
"""

from typing import Any, List

from pydantic import BaseModel, Field, field_validator


# ============================================================
# Match Request
# ============================================================

class MatchRequest(BaseModel):
    """
    Request payload for resume-job matching.
    """

    resume_text: str = Field(
        ...,
        min_length=1,
        description="Resume text or path to a resume document.",
    )

    job_description: str = Field(
        ...,
        min_length=1,
        description="Job description text.",
    )

    @field_validator("resume_text", "job_description")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        """
        Reject empty and whitespace-only input.
        """

        if not value.strip():
            raise ValueError(
                "Input must contain at least one non-whitespace character."
            )

        return value


# ============================================================
# Match Response
# ============================================================

class MatchResponse(BaseModel):
    """
    Structured response returned by the matching API.
    """

    resume_name: str = Field(
        ...,
        description="Name extracted from the resume.",
    )

    job_title: str = Field(
        ...,
        description="Job title extracted from the job description.",
    )

    match_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of job skills matched by the resume.",
    )

    matched_skills: List[str] = Field(
        default_factory=list,
        description="Skills present in both the resume and job description.",
    )

    missing_skills: List[str] = Field(
        default_factory=list,
        description="Required job skills missing from the resume.",
    )

    extra_skills: List[str] = Field(
        default_factory=list,
        description="Resume skills not required by the job description.",
    )

    matched_count: int = Field(
        ...,
        ge=0,
        description="Number of matched skills.",
    )

    missing_count: int = Field(
        ...,
        ge=0,
        description="Number of missing job skills.",
    )

    extra_count: int = Field(
        ...,
        ge=0,
        description="Number of extra resume skills.",
    )

    skill_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Normalized skill score.",
    )

    skill_score_max: float = Field(
        ...,
        ge=0,
        description="Maximum possible skill score.",
    )

    pipeline_status: str = Field(
        ...,
        description="Pipeline execution status.",
    )


# ============================================================
# Health Response
# ============================================================

class HealthResponse(BaseModel):
    """
    Response schema for API health check.
    """

    status: str
    service: str


# ============================================================
# Error Response
# ============================================================

class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    error: str = Field(
        ...,
        description="Short error type.",
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
    )

    details: Any | None = Field(
        default=None,
        description="Additional error details.",
    )
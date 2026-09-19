"""
Health check route for the AI Resume Job Matcher API.
"""

from fastapi import APIRouter

from api.schemas import HealthResponse


# ============================================================
# Router
# ============================================================

router = APIRouter(
    tags=["Health"],
)


# ============================================================
# Health Check
# ============================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check whether the AI Resume Job Matcher API is running.",
)
def health_check() -> HealthResponse:
    """
    Return the current API health status.
    """

    return HealthResponse(
        status="healthy",
        service="ai-resume-job-matcher",
    )
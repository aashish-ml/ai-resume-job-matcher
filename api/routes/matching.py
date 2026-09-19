"""
Resume-job matching API routes.
"""

from fastapi import APIRouter, HTTPException

from api.schemas import MatchRequest, MatchResponse
from src.pipeline.matcher_pipeline import run_matching_pipeline
from src.utils.logger import logger


# ============================================================
# Router
# ============================================================

router = APIRouter(
    tags=["Matching"],
)


# ============================================================
# Resume-Job Matching
# ============================================================

@router.post(
    "/match",
    response_model=MatchResponse,
    summary="Match Resume to Job",
    description=(
        "Analyze a resume against a job description and return "
        "matched skills, missing skills, extra skills, and "
        "the overall skill match percentage."
    ),
    responses={
        400: {
            "description": "Invalid matching request.",
        },
        422: {
            "description": "Request validation failed.",
        },
        500: {
            "description": "Internal server error.",
        },
    },
)
def match_resume_to_job(
    request: MatchRequest,
) -> MatchResponse:
    """
    Match a resume against a job description.
    """

    try:
        logger.info(
            "Received resume-job matching API request"
        )

        result = run_matching_pipeline(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )

        logger.info(
            "Resume-job matching API request completed"
        )

        return MatchResponse(**result)

    except ValueError as exc:

        logger.warning(
            "Invalid matching request: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        logger.exception(
            "Resume-job matching API request failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc
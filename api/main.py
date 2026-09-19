"""
FastAPI application for the AI Resume Job Matcher.

Exposes the resume-job matching pipeline through HTTP endpoints.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.routes.health import router as health_router
from api.schemas import ErrorResponse, MatchRequest, MatchResponse
from src.pipeline.matcher_pipeline import run_matching_pipeline
from src.utils.logger import logger


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Resume Job Matcher API",
    description=(
        "Production-oriented API for matching resumes with job "
        "descriptions using skill extraction, skill matching "
        "and scoring."
    ),
    version="1.0.0",
)


# ============================================================
# Routers
# ============================================================

app.include_router(health_router)


# ============================================================
# Global Validation Error Handler
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Return a clean and consistent JSON response
    for request validation errors.
    """

    details = []

    for error in exc.errors():
        details.append(
            {
                "type": error.get("type"),
                "loc": list(error.get("loc", [])),
                "msg": error.get("msg"),
                "input": error.get("input"),
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed.",
            "details": details,
        },
    )


# ============================================================
# Global Unexpected Error Handler
# ============================================================

@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected application errors consistently.
    """

    logger.exception(
        "Unhandled API exception: %s",
        exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Internal server error.",
            "details": None,
        },
    )


# ============================================================
# Resume-Job Matching Endpoint
# ============================================================

@app.post(
    "/match",
    response_model=MatchResponse,
    summary="Match Resume to Job",
    description=(
        "Analyze a resume against a job description and return "
        "matched skills, missing skills, extra skills and "
        "the overall skill match percentage."
    ),
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid matching request.",
        },
        422: {
            "model": ErrorResponse,
            "description": "Request validation failed.",
        },
        500: {
            "model": ErrorResponse,
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

    logger.info(
        "Received resume-job matching API request"
    )

    try:
        result = run_matching_pipeline(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )

        logger.info(
            "Resume-job matching API request completed successfully"
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
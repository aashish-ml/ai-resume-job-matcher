"""
Resume → Job Matching Orchestration Pipeline.

Connects ingestion, preprocessing, extraction,
matching, and scoring components into one workflow.
"""

from pathlib import Path
from typing import Any, Dict

from src.ingestion.document_loader import load_document
from src.preprocessing.pipeline import preprocess_resume
from src.extraction.resume_extractor import extract_resume_data
from src.extraction.skill_extractor import extract_skills
from src.extraction.job_extractor import extract_job_data
from src.matching.skill_matcher import match_skills
from src.scoring.score_engine import calculate_skill_score, build_match_result

from src.utils.logger import logger


def _resolve_resume_text(resume_input: str) -> str:
    """
    Resolve resume input into actual resume text.

    The pipeline accepts either:
    1. Raw resume text
    2. A path to a resume document
    """

    if not isinstance(resume_input, str):
        raise ValueError(
            "resume_input must be a string."
        )

    if not resume_input.strip():
        raise ValueError(
            "resume_input must not be empty."
        )

    candidate_path = Path(resume_input)

    # ---------------------------------------------------------
    # If input is an existing file, load its contents.
    # ---------------------------------------------------------

    if candidate_path.is_file():
        logger.info(
            "Resume input detected as file path: %s",
            candidate_path,
        )

        resume_text = load_document(str(candidate_path))

        if not isinstance(resume_text, str) or not resume_text.strip():
            raise ValueError(
                "Resume document was loaded but contains no text."
            )

        return resume_text

    # ---------------------------------------------------------
    # Otherwise treat input as raw resume text.
    # ---------------------------------------------------------

    logger.info(
        "Resume input detected as raw text."
    )

    return resume_input


def run_matching_pipeline(
    resume_text: str,
    job_description: str,
) -> Dict[str, Any]:
    """
    Execute the complete resume-job matching pipeline.

    Parameters
    ----------
    resume_text:
        Raw resume text OR path to a resume document.

    job_description:
        Raw job description text.

    Returns
    -------
    Dict[str, Any]
        Final structured resume-job matching result.
    """

    # ---------------------------------------------------------
    # Step 0: Input validation
    # ---------------------------------------------------------

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError(
            "resume_text must be a non-empty string."
        )

    if not isinstance(job_description, str) or not job_description.strip():
        raise ValueError(
            "job_description must be a non-empty string."
        )

    logger.info(
        "Starting resume-job matching pipeline"
    )

    try:

        # -----------------------------------------------------
        # Step 1: Resolve resume input
        # -----------------------------------------------------

        resolved_resume_text = _resolve_resume_text(
            resume_text
        )

        logger.info(
            "Resume text resolved successfully (%d characters)",
            len(resolved_resume_text),
        )

        # -----------------------------------------------------
        # Step 2: Resume preprocessing
        # -----------------------------------------------------

        preprocessing_result = preprocess_resume(
            resolved_resume_text
        )

        sections = preprocessing_result["sections"]

        logger.info(
            "Resume preprocessing completed: %d sections",
            len(sections),
        )

        # -----------------------------------------------------
        # Step 3: Structured resume extraction
        # -----------------------------------------------------

        resume_data = extract_resume_data(
            sections
        )

        resume_name = resume_data["name"]

        # -----------------------------------------------------
        # Step 4: Resume skill extraction
        # -----------------------------------------------------

        skills_text = sections.get(
            "skills",
            ""
        )

        # -----------------------------------------------------
        # Safety fallback
        # -----------------------------------------------------

        # Some resumes may not have an explicit "Skills"
        # heading. In that case, use the full cleaned resume
        # text so the skill extractor can still identify skills.

        if not skills_text.strip():

            logger.warning(
                "Skills section not found. "
                "Using full resume text for skill extraction."
            )

            skills_text = resolved_resume_text

        resume_skills = extract_skills(
            skills_text
        )

        logger.info(
            "Resume skill extraction completed: %d skills found",
            len(resume_skills),
        )

        # -----------------------------------------------------
        # Step 5: Job description extraction
        # -----------------------------------------------------

        job_data = extract_job_data(
            job_description
        )

        job_title = job_data["title"]
        job_skills = job_data["skills"]

        logger.info(
            "Job description extraction completed: %d skills found",
            len(job_skills),
        )

        # -----------------------------------------------------
        # Step 6: Skill matching
        # -----------------------------------------------------

        matching_result = match_skills(
            resume_skills,
            job_skills,
        )

        logger.info(
            "Skill matching completed: %.2f%% match",
            matching_result["match_percentage"],
        )

        # -----------------------------------------------------
        # Step 7: Skill score calculation
        # -----------------------------------------------------

        score_result = calculate_skill_score(
            matching_result["match_percentage"]
        )

        logger.info(
            "Skill score calculated: %.2f/100",
            score_result["skill_score"],
        )

        # -----------------------------------------------------
        # Step 8: Build final result
        # -----------------------------------------------------

        final_result = build_match_result(
            resume_name=resume_name,
            job_title=job_title,
            matching_result=matching_result,
        )

        # -----------------------------------------------------
        # Step 9: Add score information
        # -----------------------------------------------------

        final_result["skill_score"] = (
            score_result["skill_score"]
        )

        final_result["skill_score_max"] = (
            score_result["skill_score_max"]
        )

        # -----------------------------------------------------
        # Step 10: Pipeline metadata
        # -----------------------------------------------------

        final_result["pipeline_status"] = "success"

        logger.info(
            "Resume-job matching pipeline completed successfully"
        )

        return final_result

    except Exception as exc:

        logger.exception(
            "Resume-job matching pipeline failed"
        )

        raise
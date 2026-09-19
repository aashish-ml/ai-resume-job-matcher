from typing import Dict

from src.utils.logger import logger


class ScoringError(Exception):
    """Raised when resume-job scoring fails."""


def calculate_skill_score(
    match_percentage: float,
) -> Dict[str, object]:
    """
    Calculate the normalized skill score.

    Parameters
    ----------
    match_percentage : float
        Percentage of required job skills matched
        by the candidate.

    Returns
    -------
    Dict[str, object]
        Skill score details.
    """

    if not isinstance(match_percentage, (int, float)):
        raise ScoringError(
            "match_percentage must be a number."
        )

    if match_percentage < 0 or match_percentage > 100:
        raise ScoringError(
            "match_percentage must be between 0 and 100."
        )

    try:
        logger.info(
            "Calculating skill score from %.2f%% match",
            match_percentage,
        )

        score = round(float(match_percentage), 2)

        result = {
            "skill_score": score,
            "skill_score_max": 100.0,
            "match_percentage": score,
        }

        logger.info(
            "Skill score calculated: %.2f/100",
            score,
        )

        return result

    except ScoringError:
        raise

    except Exception as exc:
        logger.exception(
            "Skill score calculation failed"
        )

        raise ScoringError(
            f"Failed to calculate skill score: {exc}"
        ) from exc

def build_match_result(
    resume_name: str,
    job_title: str,
    matching_result: dict[str, object],
) -> dict[str, object]:
    if not isinstance(resume_name, str) or not resume_name.strip():
        raise ScoringError(
            "resume_name must be a non-empty string."
        )

    if not isinstance(job_title, str) or not job_title.strip():
        raise ScoringError(
            "job_title must be a non-empty string."
        )

    if not isinstance(matching_result, dict):
        raise ScoringError(
            "matching_result must be a dictionary."
        )

    try:
        match_percentage = float(
            matching_result.get("match_percentage", 0.0)
        )

        matched_skills = matching_result.get(
            "matched_skills",
            [],
        )

        missing_skills = matching_result.get(
            "missing_skills",
            [],
        )

        extra_skills = matching_result.get(
            "extra_skills",
            [],
        )

        result = {
            "resume_name": resume_name.strip(),
            "job_title": job_title.strip(),
            "match_percentage": round(match_percentage, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
            "extra_count": len(extra_skills),
        }

        logger.info(
            "Final match result built: %.2f%%",
            match_percentage,
        )

        return result

    except Exception as exc:
        logger.exception(
            "Failed to build final match result"
        )

        raise ScoringError(
            f"Failed to build match result: {exc}"
        ) from exc
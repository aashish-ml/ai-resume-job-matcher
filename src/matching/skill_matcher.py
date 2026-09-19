from typing import Dict, List

from src.utils.logger import logger


class SkillMatchingError(Exception):
    """Raised when skill matching fails."""


def match_skills(
    resume_skills: List[str],
    job_skills: List[str],
) -> Dict[str, object]:
    """
    Compare resume skills against required job skills.

    Parameters
    ----------
    resume_skills : List[str]
        Skills extracted from the candidate resume.

    job_skills : List[str]
        Skills required by the job description.

    Returns
    -------
    Dict[str, object]
        Matching results including matched skills,
        missing skills and match percentage.
    """

    if not isinstance(resume_skills, list):
        raise SkillMatchingError(
            "resume_skills must be a list."
        )

    if not isinstance(job_skills, list):
        raise SkillMatchingError(
            "job_skills must be a list."
        )

    if not job_skills:
        raise SkillMatchingError(
            "job_skills cannot be empty."
        )

    try:
        logger.info(
            "Starting skill matching: resume=%d, job=%d",
            len(resume_skills),
            len(job_skills),
        )

        resume_set = {
            skill.strip().lower()
            for skill in resume_skills
            if isinstance(skill, str) and skill.strip()
        }

        job_set = {
            skill.strip().lower()
            for skill in job_skills
            if isinstance(skill, str) and skill.strip()
        }

        matched_skills = sorted(
            resume_set.intersection(job_set)
        )

        missing_skills = sorted(
            job_set.difference(resume_set)
        )

        extra_skills = sorted(
            resume_set.difference(job_set)
        )

        total_required = len(job_set)

        match_percentage = (
            len(matched_skills) / total_required * 100
            if total_required > 0
            else 0.0
        )

        result = {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
            "required_count": total_required,
            "match_percentage": round(
                match_percentage,
                2,
            ),
        }

        logger.info(
            "Skill matching completed: %.2f%% match",
            result["match_percentage"],
        )

        return result

    except SkillMatchingError:
        raise

    except Exception as exc:
        logger.exception(
            "Skill matching failed"
        )

        raise SkillMatchingError(
            f"Failed to match skills: {exc}"
        ) from exc
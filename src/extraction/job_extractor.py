from typing import Dict, List

from src.utils.logger import logger


class JobExtractionError(Exception):
    """Raised when job description extraction fails."""


KNOWN_SKILLS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "computer vision",
    "data science",
    "data analysis",
    "data visualization",
    "generative ai",
    "prompt engineering",
    "power bi",
    "scikit-learn",
    "fastapi",
    "rest api",
    "sql",
    "python",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "tensorflow",
    "pytorch",
    "keras",
    "xgboost",
    "lightgbm",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "excel",
]


def extract_job_data(text: str) -> Dict[str, object]:
    """
    Extract structured information from a job description.

    Parameters
    ----------
    text : str
        Raw job description text.

    Returns
    -------
    Dict[str, object]
        Structured job information including detected skills.
    """

    if not isinstance(text, str):
        raise JobExtractionError(
            "Job description input must be a string."
        )

    if not text.strip():
        raise JobExtractionError(
            "Job description input is empty."
        )

    try:
        logger.info(
            "Starting job description extraction (%d characters)",
            len(text),
        )

        normalized_text = " ".join(
            text.lower().split()
        )

        detected_skills: List[str] = []

        for skill in KNOWN_SKILLS:
            if skill in normalized_text:
                detected_skills.append(skill)

        result = {
            "title": _extract_job_title(text),
            "skills": detected_skills,
            "skill_count": len(detected_skills),
            "description": text.strip(),
        }

        logger.info(
            "Job description extraction completed: %d skills found",
            len(detected_skills),
        )

        return result

    except JobExtractionError:
        raise

    except Exception as exc:
        logger.exception(
            "Job description extraction failed"
        )

        raise JobExtractionError(
            f"Failed to extract job description: {exc}"
        ) from exc


def _extract_job_title(text: str) -> str:
    """
    Extract a likely job title from the first meaningful line.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Unknown"

    first_line = lines[0]

    title_keywords = [
        "engineer",
        "developer",
        "analyst",
        "scientist",
        "manager",
        "intern",
        "specialist",
        "architect",
    ]

    if any(
        keyword in first_line.lower()
        for keyword in title_keywords
    ):
        return first_line

    return first_line
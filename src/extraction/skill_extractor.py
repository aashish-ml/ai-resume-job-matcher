from typing import List

from src.utils.logger import logger


class SkillExtractionError(Exception):
    """Raised when skill extraction fails."""


# Common multi-word skills must be checked before
# single-word skills.
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


def extract_skills(text: str) -> List[str]:
    """
    Extract known technical skills from resume text.

    Parameters
    ----------
    text : str
        Resume text or skills section.

    Returns
    -------
    List[str]
        Unique detected skills.
    """

    if not isinstance(text, str):
        raise SkillExtractionError(
            "Skill extraction input must be a string."
        )

    if not text.strip():
        raise SkillExtractionError(
            "Skill extraction input is empty."
        )

    try:
        logger.info(
            "Starting skill extraction (%d characters)",
            len(text),
        )

        normalized_text = " ".join(
            text.lower().split()
        )

        detected_skills = []

        for skill in KNOWN_SKILLS:
            if skill in normalized_text:
                detected_skills.append(skill)

        logger.info(
            "Skill extraction completed: %d skills found",
            len(detected_skills),
        )

        return detected_skills

    except SkillExtractionError:
        raise

    except Exception as exc:
        logger.exception(
            "Skill extraction failed"
        )

        raise SkillExtractionError(
            f"Failed to extract skills: {exc}"
        ) from exc
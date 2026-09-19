from typing import Dict, Any

from src.utils.logger import logger


class ResumeExtractionError(Exception):
    """Raised when structured resume extraction fails."""


def extract_resume_data(
    sections: Dict[str, str],
) -> Dict[str, Any]:
    """
    Convert detected resume sections into structured resume data.

    Parameters
    ----------
    sections : Dict[str, str]
        Resume sections produced by the preprocessing pipeline.

    Returns
    -------
    Dict[str, Any]
        Structured resume information.
    """

    if not isinstance(sections, dict):
        raise ResumeExtractionError(
            "Resume sections must be provided as a dictionary."
        )

    if not sections:
        raise ResumeExtractionError(
            "Resume sections are empty."
        )

    try:
        logger.info(
            "Starting structured resume extraction"
        )

        header = sections.get("header", "").strip()

        skills = sections.get("skills", "").strip()
        experience = sections.get("experience", "").strip()
        projects = sections.get("projects", "").strip()
        education = sections.get("education", "").strip()
        certifications = sections.get(
            "certifications", ""
        ).strip()
        languages = sections.get("languages", "").strip()

        # ---------------------------------------------------------
        # Extract name and professional title from header
        # ---------------------------------------------------------

        header_lines = [
            line.strip()
            for line in header.splitlines()
            if line.strip()
        ]

        name = ""
        title = ""

        if header_lines:
            name = header_lines[0]

        if len(header_lines) >= 2:
            title = header_lines[1]

        result = {
            "name": name,
            "title": title,
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "education": education,
            "certifications": certifications,
            "languages": languages,
        }

        logger.info(
            "Structured resume extraction completed"
        )

        return result

    except ResumeExtractionError:
        raise

    except Exception as exc:
        logger.exception(
            "Structured resume extraction failed"
        )

        raise ResumeExtractionError(
            f"Failed to extract resume data: {exc}"
        ) from exc
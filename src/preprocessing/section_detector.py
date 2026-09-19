import re
from typing import Dict

from src.utils.logger import logger


class SectionDetectionError(Exception):
    """Raised when resume section detection fails."""


# Common resume section headings.
SECTION_ALIASES = {
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "about me",
        "objective",
        "career objective",
    },
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "skills & technologies",
        "technical expertise",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "work history",
    },
    "education": {
        "education",
        "academic background",
        "academic qualification",
        "qualifications",
        "educational background",
    },
    "projects": {
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "project experience",
    },
    "certifications": {
        "certification",
        "certifications",
        "certificate",
        "certificates",
        "professional certification",
        "professional certifications",
        "licenses & certifications",
    },
    "achievements": {
        "achievements",
        "accomplishments",
        "awards",
        "honors",
    },
    "languages": {
        "languages",
        "language",
        "language proficiency",
    },
    "interests": {
        "interests",
        "hobbies",
        "hobbies & interests",
    },
}


def _normalize_heading(line: str) -> str:
    """Normalize a possible section heading."""

    value = line.strip().lower()

    # Remove common heading punctuation.
    value = re.sub(r"[:\-|]+$", "", value)

    # Normalize whitespace.
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def detect_section_heading(line: str) -> str | None:
    """
    Detect whether a line represents a known resume section.

    Supports both:

        Skills

    and:

        Skills: Python, SQL, Machine Learning

    Returns
    -------
    str | None
        Canonical section name or None.
    """

    normalized = _normalize_heading(line)

    if not normalized:
        return None

    # ---------------------------------------------------------
    # Exact heading match
    # ---------------------------------------------------------
    for section_name, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return section_name

    # ---------------------------------------------------------
    # Heading followed by content
    #
    # Example:
    # Skills: Python, SQL
    # Education: Bachelor of Arts
    # Projects: Built an ML system
    # ---------------------------------------------------------
    for section_name, aliases in SECTION_ALIASES.items():
        for alias in aliases:

            # Match:
            # "skills: ..."
            # "education - ..."
            # "projects | ..."
            pattern = rf"^{re.escape(alias)}\s*[:\-|]\s*.+$"

            if re.match(pattern, normalized):
                return section_name

    return None


def _extract_inline_section_content(line: str, section_name: str) -> str:
    """
    Extract content appearing after an inline section heading.

    Example:
        Skills: Python, SQL

    Returns:
        Python, SQL
    """

    normalized_line = line.strip()

    aliases = SECTION_ALIASES.get(section_name, set())

    for alias in aliases:
        pattern = rf"^{re.escape(alias)}\s*[:\-|]\s*(.*)$"

        match = re.match(
            pattern,
            normalized_line,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return ""


def detect_sections(text: str) -> Dict[str, str]:
    """
    Split resume text into logical sections.

    Supports both standalone headings and inline headings.

    Examples:

        Skills
        Python, SQL, FastAPI

    and:

        Skills: Python, SQL, FastAPI

    Text before the first recognized heading is stored under
    the 'header' section.
    """

    if not isinstance(text, str):
        raise SectionDetectionError(
            "Input text must be a string."
        )

    if not text.strip():
        raise SectionDetectionError(
            "Input text is empty."
        )

    try:
        logger.info(
            "Starting section detection (%d characters)",
            len(text),
        )

        # ---------------------------------------------------------
        # Normalize escaped newline characters
        # ---------------------------------------------------------
        text = text.replace("\\r\\n", "\n")
        text = text.replace("\\n", "\n")
        text = text.replace("\\r", "\n")

        lines = text.splitlines()

        sections: Dict[str, list[str]] = {}

        current_section = "header"

        sections[current_section] = []

        # ---------------------------------------------------------
        # Process every line
        # ---------------------------------------------------------
        for line in lines:

            stripped_line = line.strip()

            if not stripped_line:
                continue

            heading = detect_section_heading(stripped_line)

            # -----------------------------------------------------
            # Recognized section heading
            # -----------------------------------------------------
            if heading:

                current_section = heading

                if current_section not in sections:
                    sections[current_section] = []

                # -------------------------------------------------
                # Handle inline content
                #
                # Example:
                # Skills: Python, SQL
                # -------------------------------------------------
                inline_content = _extract_inline_section_content(
                    stripped_line,
                    heading,
                )

                if inline_content:
                    sections[current_section].append(
                        inline_content
                    )

                continue

            # -----------------------------------------------------
            # Normal content
            # -----------------------------------------------------
            sections[current_section].append(
                stripped_line
            )

        # ---------------------------------------------------------
        # Convert lists into clean strings
        # ---------------------------------------------------------
        result: Dict[str, str] = {}

        for section_name, content in sections.items():

            cleaned_content = "\n".join(
                content
            ).strip()

            if cleaned_content:
                result[section_name] = cleaned_content

        logger.info(
            "Section detection completed: %d sections found",
            len(result),
        )

        return result

    except SectionDetectionError:
        raise

    except Exception as exc:

        logger.exception(
            "Section detection failed"
        )

        raise SectionDetectionError(
            f"Failed to detect resume sections: {exc}"
        ) from exc
import re

from src.utils.logger import logger


class TextCleaningError(Exception):
    """Raised when text cleaning fails."""


def clean_text(text: str) -> str:
    """
    Clean extracted resume/job-description text.

    The cleaning process intentionally preserves:
    - technical terms
    - numbers
    - punctuation useful for technologies
    - hyphenated terms
    - programming/library names

    Parameters
    ----------
    text : str
        Raw extracted document text.

    Returns
    -------
    str
        Cleaned text.
    """

    if not isinstance(text, str):
        raise TextCleaningError(
            "Input text must be a string."
        )

    if not text.strip():
        raise TextCleaningError(
            "Input text is empty."
        )

    try:
        logger.info(
            "Starting text cleaning (%d characters)",
            len(text),
        )

        cleaned = text

        # -----------------------------------------------------
        # Normalize line endings
        # -----------------------------------------------------

        cleaned = cleaned.replace("\r\n", "\n")
        cleaned = cleaned.replace("\r", "\n")

        # -----------------------------------------------------
        # Replace tabs with spaces
        # -----------------------------------------------------

        cleaned = cleaned.replace("\t", " ")

        # -----------------------------------------------------
        # Normalize excessive whitespace
        # -----------------------------------------------------

        cleaned = re.sub(
            r"[ ]{2,}",
            " ",
            cleaned,
        )

        # -----------------------------------------------------
        # Remove excessive blank lines
        # -----------------------------------------------------

        cleaned = re.sub(
            r"\n{3,}",
            "\n\n",
            cleaned,
        )

        # -----------------------------------------------------
        # Normalize spaces around line breaks
        # -----------------------------------------------------

        cleaned = re.sub(
            r" *\n *",
            "\n",
            cleaned,
        )

        # -----------------------------------------------------
        # Remove non-printable control characters
        # while preserving newlines and tabs already handled.
        # -----------------------------------------------------

        cleaned = "".join(
            char
            for char in cleaned
            if char == "\n" or char.isprintable()
        )

        # -----------------------------------------------------
        # Final cleanup
        # -----------------------------------------------------

        cleaned = cleaned.strip()

        if not cleaned:
            raise TextCleaningError(
                "Text became empty after cleaning."
            )

        logger.info(
            "Text cleaning completed (%d characters)",
            len(cleaned),
        )

        return cleaned

    except TextCleaningError:
        raise

    except Exception as exc:
        logger.exception(
            "Text cleaning failed"
        )

        raise TextCleaningError(
            f"Failed to clean text: {exc}"
        ) from exc